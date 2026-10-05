# © 2023 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
# http://aws.amazon.com/agreement or other written agreement between Customer and either
# Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

# ==============================================================================================
# Trigger:
#   • view request
#       • /lny/?type=fit
#       • /lny/?type=new
#       • /*submit-CNY
# Purpose:
#   • check reqesut, origin health, capacity-available, generate JWT payload update users table.
# ==============================================================================================
import os
import sys
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import uuid
import re
import time
from common.libs.print_helper import print
from common.libs import dynamodb_helper
from common.libs import x_helper

def lambda_handler(event, _):
    x_helper.print_json(event)
    if x_helper.is_warmup(event):
        print("############### warmup request ##############", log_level='info')
        time.sleep(2)
        x_helper.trigger_update_capacity_lambda(warmup=True)
        return x_helper.redirect(x_helper.read_only_url)

    if not x_helper.check_schedule():
        return x_helper.redirect(x_helper.read_only_url)

    request = event['Records'][0]['cf']['request']
    uri = request['uri']
    if re.match(r'/lny/.*', uri):
        return lny_handler(event)
    elif re.match(r'/.*submit-CNY', uri):
        return submit_handler(event)

def submit_handler(event):
    # Parse early so we can include cf_request_id in every log
    cf_request_id, request, headers, _, _, _ = x_helper.parse_event(event)

    print(f"CF Req ID:[{cf_request_id}] ############### submit viewer request ##############", log_level='info')

    access_token = x_helper.get_access_token_from_cookie(headers)

    if not access_token:
        print(f"CF Req ID:[{cf_request_id}] No access token found in cookie. Redirecting to landing. "
              f"URL='{x_helper.landing_url}'",
              log_level='info')
        return x_helper.redirect(x_helper.landing_url)

    # Validate token before using any of its fields
    if x_helper.token_invalid_or_expired(access_token):
        print(f"CF Req ID:[{cf_request_id}] Access token is invalid or expired.", log_level='warning')

        # We don't know note_type safely yet; redirect to a generic timeout
        # OR decode safely and fall back if missing
        safe_note_type = x_helper.get_type_from_token_safe(access_token)

        if safe_note_type:
            timeout_url = x_helper.timeout_error_url(safe_note_type)
            print(
                f"CF Req ID:[{cf_request_id}] Redirecting to timeout page for note_type='{safe_note_type}'. "
                f"URL='{timeout_url}'",
                log_level='info'
            )
            return x_helper.redirect(timeout_url)
        else:
            # Choose a generic timeout URL without type if you have one;
            # else default to landing or a specific type.
            print(
                f"CF Req ID:[{cf_request_id}] No safe note_type available from token. "
                f"Redirecting to landing page. URL='{x_helper.landing_url}'",
                log_level='info'
            )
            return x_helper.redirect(x_helper.landing_url)

    # After validation, now it’s safe to read noteType
    note_type = x_helper.get_type_from_token(access_token)

    payload = x_helper.decrpt_jwt_token(access_token)
    user_item = dynamodb_helper.get_user_by_id(payload['uuid'])
    user_item['RequestId'] = cf_request_id
    dynamodb_helper.create_or_update_user(user_item)

    print(f"CF Req ID:[{cf_request_id}] ############### request to origin ##############", log_level='info')
    x_helper.print_json(request)
    return request

def lny_handler(event):
    print("############### lny viewer request ##############", log_level='info')
    cf_request_id,request,headers,querystring,_,_ = x_helper.parse_event(event)
    _,current_time_epoch,_,expiry_time_epoch = x_helper.get_times()
    note_type = x_helper.get_type_from_querystring(querystring)
    # no queryString
    if not note_type:
        return x_helper.redirect(x_helper.landing_url)

    # if x_helper.slot_is_full(note_type):
    #     return x_helper.redirect(x_helper.thank_you_url(note_type))

    is_healthy = x_helper.origin_is_healthy()
    print(f"############### origin healthy {is_healthy} ##############", log_level='info')
    access_token = x_helper.get_access_token_from_cookie(headers)
    user_item = {}
    if access_token:
        if x_helper.token_invalid_or_expired(access_token):
            return x_helper.redirect(x_helper.timeout_error_url(note_type))
        note_type_from_token = x_helper.get_type_from_token(access_token)
        if note_type_from_token != note_type:
            return x_helper.redirect(x_helper.note_type_not_match_url(note_type_from_token), jwt_token=access_token)
        payload = x_helper.decrpt_jwt_token(access_token)
        user_item = dynamodb_helper.get_user_by_id(payload['uuid'])

    def generate_users_item(user_item):
        user_item['Uuid'] = payload['uuid']
        user_item['Allowed'] = payload['allowed']
        user_item['ExpiryTime'] = payload['expiryTime']
        user_item['NoteType'] = payload['noteType']
        user_item['EntryTime'] = user_item.get('EntryTime', current_time_epoch)
        user_item['RequestId'] = cf_request_id
        user_item['Jwt'] = x_helper.generate_jwt_token(payload)
         # Handle hot parition key issue in GSI Allowed-QueueNumber-index by write sharding
        user_item['GsiAllowedPk'] = random.choice(dynamodb_helper.gsi_allowed_keys(payload['allowed']))
        return user_item

    def form_available_process(user_item):
        print("############### available ##############", log_level='info')
        r = x_helper.reduce_available_capacity()
        if not r:
            print(r)
            print("############### capacity already changed by other requests, move to not_available_process ##############", log_level='info')
            return form_not_available_process(user_item)
        payload['allowed'] = 'true'
        payload['expiryTime'] = expiry_time_epoch
        payload['noteType'] = note_type
        print(f"############### payload before update to user: {payload} ##############", log_level='info')
        user_item = generate_users_item(user_item)
        dynamodb_helper.create_or_update_user(user_item)
        print("############### request to origin ##############", log_level='info')
        x_helper.print_json(request)
        return request

    def form_not_available_process(user_item):
        print("############### not available ##############", log_level='info')
        payload['allowed'] = 'false'
        payload['expiryTime'] = expiry_time_epoch
        payload['noteType'] = note_type
        print(f"############### payload before update to user: {payload} ##############", log_level='info')
        user_item = generate_users_item(user_item)
        dynamodb_helper.create_or_update_user(user_item)
        print("############### redirect to waiting-room page ##############")
        return x_helper.redirect(x_helper.waiting_room_url(note_type), user_item['Jwt'])

    if not access_token: # first request
        print("############### first time ##############", log_level='info')
        payload = {
            'uuid': str(uuid.uuid4())
        }
    else: # token exisiting, not first time
        print("############### not first time ##############", log_level='info')
        if user_item.get('Allowed') == 'true':
            print("############### user already allowed, pass the request ##############", log_level='info')
            x_helper.print_json(request)
            return request

    available_capacity = dynamodb_helper.get_real_available_capacity()
    user_count_before = x_helper.count_user_before(user_item)
    print(f"############### capacity {available_capacity} users count before {user_count_before} ##############", log_level='info')
    form_available = is_healthy and available_capacity > user_count_before
    if form_available:
        return form_available_process(user_item)
    else: # not healthy or no slot
        return form_not_available_process(user_item)