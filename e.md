**Subject: [NO ACTION REQUIRED] Upcoming AWS Network ACL (NACL) Changes - Security Remediation**

Dear Application Owners and Technical Teams,

We are writing to inform you of upcoming changes to AWS Network Access Control Lists (NACLs) across workload accounts as part of a security remediation initiative. This email contains information about the changes.


## WHAT IS CHANGING?

We will be updating Network ACL configurations for private subnets in your AWS workload accounts to address security findings. The changes include:

**Configuration Updates:**
- Adding ephemeral port rules (TCP/UDP 1024-65535) for return traffic
- Adding outbound HTTPS rules (TCP port 443)
- Adding both inbound and outbound to private subnets
- Adding SSH (22) and RDP (3389) deny rules for inbound traffic. Only allowing connection from private subnets. 
- Adding private subnet ranges (10.0.0.0/8, 192.168.0.0/16, 100.64.0.0/16) ALLOW rules
- Restricting overly permissive 0.0.0.0/0 rules
- Ensuring proper bidirectional traffic flow for stateless NACLs

**Affected Resources:**
- Network ACLs attached to private subnets in your VPC
- Accounts across all Landing Zone Portfolios: 
Note: These NACLs are managed centrally in the Network Account [Account ID] and shared to workload accounts.

Lis fo NACLS:
- NACL IDs: [List of NACL IDs]

***

## IMPLEMENTATION TIMELINE
November 9, 2025 9-am to 6-pm GMT (Green Zone)

***

## EXPECTED IMPACT

**Overall Risk Level: LOW**

Based on  VPC Flow Log analysis:
- **No WAN (internet) outbound traffic** detected from private subnets
- Private subnets have no direct internet access, significantly reducing risk
- Changes primarily add missing rules rather than fully restricting all existing traffic
- No application downtime expected


## WHAT DO APPLICATION OWNERS NEED TO DO?

### NO REQUIRED ACTIONS

## COMMUNICATION AND SUPPORT

**Questions or Concerns:**
- Email: [your-team-email@company.com]


## ROLLBACK PLAN

We have comprehensive rollback procedures in place:
- **Rollback Time:** <5 minutes per NACL
- **Availability:** Immediate during implementation window
- **Retention:** Previous configurations saved for 30 days
- **Trigger:** Any confirmed application connectivity issue

***

## WHY ARE WE MAKING THESE CHANGES?

**Security Compliance:** Address findings from security audit to meet organizational security standards

**Best Practices:** Align NACL configurations with AWS and industry best practices

***


Thank you for your cooperation in this important security initiative. We have taken extensive precautions to ensure minimal impact, including VPC Flow Log analysis, phased implementation, and immediate rollback capabilities.

If you have any questions or concerns, please don't hesitate to reach out using the contact information provided above.

Best regards,

**[Your Name]**  
AWS Cloud Infrastructure Team  
[Your Email]  
[Your Phone]  

***
