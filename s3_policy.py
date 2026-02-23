#!/usr/bin/env python3
import json
import sys
import boto3
import botocore


def assume_role(admin_role_arn: str, session_name: str = "AdminSession"):
    """
    Assume the specified IAM role and return a boto3.Session
    created with the temporary credentials.
    """
    sts = boto3.client("sts")
    response = sts.assume_role(
        RoleArn=admin_role_arn,
        RoleSessionName=session_name,
        DurationSeconds=3600,  # adjust if needed
    )

    creds = response["Credentials"]

    # Create a new session with the assumed role credentials
    assumed_session = boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )
    return assumed_session


def load_json_file(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    if len(sys.argv) != 5:
        print(
            f"Usage: {sys.argv[0]} <bucket-name> <new-statement.json> "
            "<region> <admin-role-arn>"
        )
        sys.exit(1)

    bucket_name = sys.argv[1]
    new_stmt_path = sys.argv[2]
    region = sys.argv[3]
    admin_role_arn = sys.argv[4]

    # 1. Assume the admin role
    admin_session = assume_role(admin_role_arn, session_name="AdminBucketPolicyUpdate")

    # 2. Use the assumed role session for S3 operations
    s3 = admin_session.client("s3", region_name=region)

    # Load new statement (must be a single JSON statement object)
    new_statement = load_json_file(new_stmt_path)

    # Get existing policy (if any)
    try:
        result = s3.get_bucket_policy(Bucket=bucket_name)
        policy_str = result["Policy"]
        policy = json.loads(policy_str)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
            policy = {
                "Version": "2012-10-17",
                "Statement": []
            }
        else:
            raise

    # Ensure Statement is a list
    if "Statement" not in policy or not isinstance(policy["Statement"], list):
        policy["Statement"] = []

    # Append new statement
    policy["Statement"].append(new_statement)

    # Convert back to string
    policy_str_new = json.dumps(policy)

    # Put updated policy
    s3.put_bucket_policy(Bucket=bucket_name, Policy=policy_str_new)

    print(
        f"Updated bucket policy for {bucket_name} using admin role "
        f"{admin_role_arn} with new statement from {new_stmt_path}"
    )


if __name__ == "__main__":
    main()
