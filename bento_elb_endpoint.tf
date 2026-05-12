# Security Group for the VPC Endpoint
resource "aws_security_group" "vpc_endpoint_sg" {
  name        = "elb-vpc-endpoint-sg"
  description = "Allow inbound HTTPS traffic from the Lambda function"
  vpc_id      =  var.vpc_id # Replace with your VPC ID

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }
}

# ---------------------------------------------------------
# VPC Endpoint for Amazon Elastic Load Balancing API
# ---------------------------------------------------------
resource "aws_vpc_endpoint" "elb_api_endpoint" {
  vpc_id            = var.vpc_id # Replace with your VPC ID
  service_name      = "com.amazonaws.ap-southeast-1.elasticloadbalancing" # Make sure this matches your region
  vpc_endpoint_type = "Interface"

  # Deploy the endpoint into the same subnets as your Lambda (or routing subnets)
  subnet_ids = [var.subnet_id_1a, var.subnet_id_1b] 
  
  security_group_ids = [
    aws_security_group.vpc_endpoint_sg.id
  ]

  # Enables private DNS routing so the default Boto3 client automatically uses this endpoint
  private_dns_enabled = true 
}

# ---------------------------------------------------------
# VPC Endpoint for Amazon SNS
# ---------------------------------------------------------

# Interface VPC Endpoint for Amazon SNS
resource "aws_vpc_endpoint" "sns_endpoint" {
  vpc_id            = var.vpc_id # Replace with your VPC ID
  service_name      = "com.amazonaws.ap-southeast-1.sns" # Ensure this matches your region
  vpc_endpoint_type = "Interface"

  # Deploy into the same subnets as your Lambda
  subnet_ids = [var.subnet_id_1a, var.subnet_id_1b]
  
  # Reuse the VPC endpoint security group you created earlier for ELB
  security_group_ids = [
    aws_security_group.vpc_endpoint_sg.id
  ]

  # Enables private DNS routing so the Boto3 SNS client automatically uses this private endpoint
  private_dns_enabled = true 
}