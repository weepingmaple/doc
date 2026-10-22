| S/N | ISRA Control Requirement for Cloud Services/Application | Provide detail of how the control requirement is met / reason if not enabled |
|------|------|------|
| 1.1 | Provide a list of connections in the "List of Connections" tab, including interactive and non-interactive access, connections to other public cloud services, and connections to external systems. | |
| 1.2 | Baseline configuration standards should be established for the cloud service. | |
| 1.3 | Describe the control in place for segregation of production and test environments. | |
| 1.4 | Where service mode is IaaS or PaaS, Bank-approved anti-virus / anti-malware and host-based intrusion prevention system should be implemented. | |
| 1.5 | Cloud service provider should ensure penetration testing has been performed covering OWASP Top vulnerabilities, CWE Top 25, and applicable API/microservice threats. | |
| 2.1 | Does the cloud service support and enable integration with the Bank's Azure Active Directory (AD) for all interactive user authentication? | |
| 2.1.1 | State the specific protocol supported for Azure AD integration (e.g. SAML 2.0). | |
| 2.1.2 | Describe the supported interactive user authentication mechanisms that will be enabled. | |
| 2.1.3 | Authentication mechanism should enforce minimum 12-character passwords with alphabetic and numeric/special characters. | |
| 2.1.4 | Password controls: non-null, no reuse of last 5 passwords, maximum validity period, mandatory expiry changes. | |
| 2.1.5 | Force password change upon first login using temporary/issued password. | |
| 2.1.6 | Passwords should be issued securely; avoid clear-text email delivery. | |
| 2.1.7 | Support password change by authenticated users at any time. | |
| 2.1.8 | Store passwords in irreversible cryptographic format using approved algorithms. | |
| 2.1.9 | Protect stored passwords using strong access controls and least privilege. | |
| 2.1.10 | Passwords must not be returned to clients in any form for verification. | |
| 2.1.11 | Protect printed passwords from disclosure and tampering. | |
| 2.1.12 | Automatically disable/lock accounts after configurable failed login attempts. | |
| 2.1.13 | Logon failure messages must not reveal whether username or password is incorrect. | |
| 2.2 | Default passwords should be changed before go-live. | |
| 2.3 | MFA should be enabled for Internet-facing services and privileged/administrative access. | |
| 2.4 | Describe non-interactive authentication mechanisms (API keys, tokens, secrets, etc.). | |
| 2.5 | Credentials used by systems/applications should support regular rotation. | |
| 2.6 | State where credentials are stored and how they are protected. | |
| 2.7 | Confirm all hard-coded or default credentials are changed before go-live. | |
| 2.8 | Unused default accounts should be deleted or disabled. | |
| 3.1 | Support central management of security policies across multiple cloud services. | |
| 3.2 | Support segregation of duties through granular administrative role assignment. | |
| 3.3 | Support maker-checker controls for user and role administration functions. | |
| 3.4 | Support maker-checker controls for sensitive functions. | |
| 3.5 | Automatically terminate idle sessions after configurable inactivity period. | |
| 3.6 | Prevent concurrent logons using the same account from different workstations. | |
| 3.7 | Automatically revoke or disable inactive accounts after 30 days. | |
| 3.8 | Enforce least privilege and deny-by-default access controls. | |
| 3.9 | Enable network access controls (e.g. IP whitelisting) where Internet access is not required. | |
| 3.10.1 | Group containers with similar risk profiles together. | |
| 3.10.2 | Adopt container-specific security solutions. | |
| 3.10.3 | Implement stringent controls for container orchestrator access. | |
| 3.11.1 | Support robust authentication and service mesh for API access control. | |
| 4.1 | Use internationally recognized cryptographic standards. | |
| 4.2 | Encrypt sensitive credentials in transit and at rest. | |
| 4.3 | Encrypt confidential or sensitive data in transit and at rest. | |
| 4.4 | Cryptographic keys should not be hardcoded. | |
| 4.5 | Support Bring Your Own Key (BYOK). | |
| 4.6 | Store cryptographic keys in FIPS140-2 Level 3 certified HSM. | |
| 4.7 | Support Bring Your Own Encryption (BYOE). | |
| 4.8 | Support secure key rotation. | |
| 4.9 | Support secure key destruction. | |
| 4.10 | Use cryptographic keys for single purposes only. | |
| 4.11 | Allow immediate key revocation, destruction, and replacement upon compromise. | |
| 4.12 | Describe controls protecting data in multi-tenant environments. | |
| 4.13 | Scan uploaded files for malware before processing or storage. | |
| 5.1 | Ensure passwords, credentials, and keys are not logged in audit trails. | |
| 5.2 | Maintain audit logs for all access and administrative activities. | |
| 5.3 | Record successful and failed security-relevant events. | |
| 5.4 | Audit records should contain required event details. | |
| 5.5 | Audit all administration activities with detailed records. | |
| 5.6 | Protect audit trails from unauthorized modification. | |
| 5.7 | Support transfer of audit logs to the Bank's SIEM. | |
| 5.8 | Support monitoring and alerting for suspicious activities. | |
| 6.1 | Implement multi-tier architecture for Internet-facing solutions. | |
| 6.2 | Implement multi-tier architecture for private leased-line connectivity. | |

Azure Services:
Virtual WAN	Azure Virutal Network	Network Security Group	Route Table	Private Endpint	Private DNS Zone	Azure Firewall	Azure Firewall Manager	Azure Bastion	Azure Front Door + WAF	Storage Account	Azure Funcions	Virtual Machine	Azure Communication Services	Event Grid	Service Bus	Entra ID	Managed Identity	Key Vault	Defender for Cloud	Azure Policy	Azure Monitor	Azure Portal	Cost Management	Event Hub	Microsoft Sentinel	Microsoft Purview	Management Group	Subscription	Log Analytics Workspace	Resource Group	DNS resolver	DDos Protection Plan	ExpressRoute

## AWS
| S/N | ISRA Control Requirement for Cloud Services/Application | Details of How the Control Requirement is Met |
|------|------|------|
| 1.1 | Provide a list of connections in the "List of Connections" tab including interactive and non-interactive access, connections to other public cloud services, and connections from public cloud services to external systems. | With the right IAM permissions, the service can be accessed from:<br>- Management Console<br>- Command Line Interface (currently not possible from UOB Laptop, only from specific on-premise servers). |
| 1.2 | Baseline configuration standards should be established for the cloud service. | Based on CIS L1 Standards. |
| 1.3 | Describe the control in place for segregation of production and test environments. | Network and IAM level segregation. Network segregation applies to services residing within VPC such as EC2 and Lambda. |
| 1.4 | Where service mode is IaaS or PaaS, Bank-approved anti-virus / anti-malware and host-based intrusion prevention system should be implemented. | Applicable only to Containers and EC2. Containers are not used yet. |
| 1.5 | Cloud service provider should ensure penetration testing has been performed covering OWASP Top Vulnerabilities, CWE Top 25 and API/Microservice threats. | TVRA for AWS is not available, but SOC1, SOC2, SOC3 and OSPAR reports are available. |
| 2.1 | Does the cloud service support integration with the Bank's Azure Active Directory (AD) for all interactive user authentication? | Yes for AWS SSO (Management Console login). SSO is then used to access all other services via IAM where permissions are granted. |
| 2.1.1 | State the protocol supported for Azure AD integration. | SAML 2.0 for AWS SSO. |
| 2.1.2 | Describe the supported interactive user authentication mechanisms that will be enabled. | Only Breakglass ID does not use AWS SSO (Azure AD) integration. Used for service recovery if Azure AD or AWS SSO fails. |
| 2.1.3 | Authentication mechanism should enforce minimum 12-character passwords with at least one alphabet and one numeric/special character. | Enforced for Breakglass IDs. SSO IDs follow Azure AD password requirements. |
| 2.1.4 | Password policy enforcement including password history, expiry and complexity. | Enforced for Breakglass IDs. SSO IDs follow Azure AD password requirements. |
| 2.1.5 | Force password change upon first login using temporary password. | During handover to GIS, new password (2-part) is registered together with 2FA. Applies to Breakglass IDs only. |
| 2.1.6 | Passwords should be issued securely. | Face-to-face handover without paper or email. Applies to Breakglass IDs only. |
| 2.1.7 | Users should be able to change their passwords after authentication. | Supported for Breakglass IDs only. |
| 2.1.8 | User passwords should be stored in irreversible cryptographic format. | Azure AD stores and manages passwords when federated. AWS IAM Identity Center uses AES-256 encryption and SHA-256 hashing. |
| 2.1.9 | Stored passwords shall be protected using least-privilege access controls. | AWS implements controls for encryption, access, retention, physical controls, mobile devices and handling requirements. Refer to AWS Artifacts such as ISO 27001, ISO 27017, SOC 2, FedRAMP and others. |
| 2.1.10 | Passwords must not be returned to clients for verification. | AWS does not return passwords. |
| 2.1.11 | Passwords should be protected from disclosure when printed. | Not applicable. Passwords are not printed because there is only one Breakglass ID. |
| 2.1.12 | User accounts should be locked after configurable failed login attempts. | Supported as part of CIS Benchmark. Applies to Breakglass IDs. Azure AD controls SSO password policies. |
| 2.1.13 | Authentication failures should not reveal whether username or password is incorrect. | Error messages do not explain the reason for failed login attempts. |
| 2.2 | Default passwords should be changed before go-live. | Completed for Breakglass IDs. |
| 2.3 | MFA should be enabled for all interactive access. | Management Console access uses Azure AD MFA via AWS SSO. CLI access is restricted to approved on-premise servers. |
| 2.4 | Strong authentication should be used for all incoming connections. | Short-lived Just-In-Time access tokens are used. AWS SSO for Management Console and IAM Roles Anywhere for AWS APIs. |
| 2.5 | Service credentials should be changeable regularly. | Only short-lived JIT access tokens are used. |
| 2.6 | State where credentials are stored and how they are protected. | Application secrets are stored in AWS Secrets Manager with encryption at rest and IAM-based access control. |
| 2.7 | Confirm all hard-coded or default credentials are changed before go-live. | Completed for Breakglass IDs. |
| 2.8 | Unused default accounts should be deleted or disabled. | Managed through the application decommissioning process. |
| 3.1 | Central management of security policies across cloud services. | CIS L1 guardrails are enforced for each cloud service provider. |
| 3.2 | Segregation of duties through granular administrative functions. | AWS IAM supports granular role-based access control. |
| 3.3 | Maker-checker control for account and role administration. | Access management is governed through IAM, OneIdentity onboarding, and maker-checker approval workflows. |
| 3.4 | Maker-checker control for sensitive functions. | Enforced through Infrastructure-as-Code review processes and IAM governance. |
| 3.5 | Session timeout after inactivity. | AWS Management Console sessions expire after one hour. |
| 3.6 | Concurrent logins using the same account should not be allowed. | Not allowed. |
| 3.7 | Inactive accounts should be disabled after 30 days. | Managed through Active Directory and Azure AD. |
| 3.8 | Enforce least privilege and deny-by-default access. | Implemented using AWS IAM and Zero Trust principles. |
| 3.9 | Network access controls such as IP whitelisting should be enabled. | AWS Management Console only accepts connections from approved UOB IP ranges and Azure AD policies. |
# 4. Data Security

| S/N | ISRA Control Requirement | Details of How the Control Requirement is Met |
|------|------|------|
| 4.1 | Only internationally recognized cryptographic standards (e.g. RSA-2048, AES-128+, SHA256+) should be used. | All AWS services with cryptographic capabilities support AES-128, AES-256 and RSA-2048. |
| 4.2 | Sensitive credentials should be encrypted during transmission and at rest. | AWS service APIs use TLS encryption (RSA-2048) and AES-256 encryption for data at rest. |
| 4.3 | Confidential or sensitive data should be encrypted during transmission and at rest. | Application payloads must be encrypted by the application itself. AWS services cannot decrypt application payloads. |
| 4.4 | Cryptographic keys should not be hardcoded within the cloud service. | AWS does not hardcode keys within its services. |
| 4.5 | Support Bring Your Own Key (BYOK). | Supported. Public cloud KMS strategy has yet to be established. |
| 4.6 | Cryptographic keys used to protect sensitive data should be stored in FIPS140-2 Level 3 certified HSM. | Application encryption keys remain on-premise. AWS services do not decrypt application payloads. |
| 4.7 | Support Bring Your Own Encryption (BYOE). | Supported through AWS KMS. |
| 4.8 | Support secure key rotation. | AWS Secrets Manager supports secure rotation of secrets and keys. |
| 4.9 | Support secure destruction of cryptographic keys. | Managed through AWS KMS key lifecycle management. |
| 4.10 | Cryptographic keys should be used for single purposes only. | Supported through AWS KMS key management controls. |
| 4.11 | Support immediate key revocation, destruction and replacement. | Supported through AWS KMS. |
| 4.12 | Describe controls protecting customer data in a multi-tenant environment. | AWS logically segregates customer environments. Hypervisor isolation, virtualized storage, disk wiping before reuse, VPC isolation, and optional encryption protect customer data. AWS certifications include MTCS, PCI, ISO 27001, ISO 27017, SOC, FedRAMP, K-ISMS and C5. |
| 4.13 | Anti-virus scanning should be performed on uploaded files before processing or storage. | Performed on-premise before file transfers. EC2 instances are protected with anti-virus software. |

# 5. Audit Trail

| S/N | ISRA Control Requirement | Details of How the Control Requirement is Met |
|------|------|------|
| 5.1 | Passwords, credentials and cryptographic key values must not be logged. | Sensitive credentials and keys are not logged by AWS native audit services. |
| 5.2 | Maintain audit logs of all user and administrative activities. | Logs collected include VPC Flow Logs, AWS API Service Logs, DNS Logs, CloudFront Logs and WAF Events. |
| 5.3 | Record successful and failed authentication, authorization, privileged administration and API access events. | Authentication attempts, authorization events, privileged actions and API access are logged. Sensitive data exports are not applicable as no PII is stored in the cloud. |
| 5.4 | Audit records must contain sufficient event details. | Includes timestamps, user identities, event types, resource access details, status indicators and partial command execution information. |
| 5.5 | Audit all administration activities and access control changes. | CloudTrail and AWS audit services provide administrator IDs, resource changes, role changes and status information. Before/after values are not always available. |
| 5.6 | Audit trails should be protected from unauthorized access and modification. | Audit logs are stored in a dedicated AWS account with restricted access. |
| 5.7 | Audit logs should be transferred to the Bank's SIEM. | Implemented. Current GSOC requirement is to forward alerts rather than all raw logs. |
| 5.8 | Monitoring and alerting should detect suspicious activities. | Implemented through AWS GuardDuty (IDS). |

# 6. Network Security

| S/N | ISRA Control Requirement | Details of How the Control Requirement is Met |
|------|------|------|
| 6.1 | Multi-tier architecture should be implemented for Internet-facing solutions. | AWS environment supports multi-tier architecture. No public-facing web servers currently exist, therefore no DMZ is currently required. If Internet-facing workloads are deployed, DMZ architecture will be implemented. |
| 6.2 | Multi-tier architecture should be implemented for private leased-line integrations with external parties. | No third-party integrations currently exist. Requirements can be implemented when such integrations are introduced. |

# AWS Services Covered

- IAM
- AWS Artifact
- Cloud9
- CloudFormation
- CloudTrail
- CloudWatch
- CodeArtifact
- CodeBuild
- CodeCommit
- CodePipeline
- Config
- Control Tower
- Cost Explorer
- Direct Connect
- DynamoDB
- EC2 Auto Scaling
- EC2
- EventBridge
- Firewall Manager
- Glue
- GuardDuty
- IAM Identity Center
- Inspector
- Kinesis Firehose
- KMS
- Lambda
- Organizations
- Resource Access Manager
- Resource Groups
- Resource Explorer
- Route 53
- Secrets Manager
- Service Catalog
- SES
- SNS
- SQS
- Systems Manager (SSM)
- Step Functions
- Security Token Service (STS)
- Support
- VPC
- WAF
- X-Ray
- ACM
- CloudFront
- Shield