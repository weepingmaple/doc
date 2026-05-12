# Package the Python code into a zip file
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_remediation_role" {
  name = "clb-timeout-remediation-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" } 
    }]
  })
}

# IAM Policy for CloudWatch Logs and ELB modification
resource "aws_iam_role_policy" "lambda_remediation_policy" {
  name = "clb-timeout-remediation-policy"
  role = aws_iam_role.lambda_remediation_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [ 
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect   = "Allow"
        Action   = "elasticloadbalancing:ModifyLoadBalancerAttributes"
        Resource = aws_elb.classic_lb.arn # Ensure aws_elb.classic_lb is defined in your state
      }
    ]
  })
}

# Add this to grant VPC access permissions to the Lambda role
resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_remediation_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "clb_remediation" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "clb-timeout-enforcer"
  role             = aws_iam_role.lambda_remediation_role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.13"
  timeout          = 10

  # Run the Lambda inside your designated VPC subnets
  vpc_config {
    subnet_ids         = [var.subnet_id_1a, var.subnet_id_1b] 
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  # Pass the SNS Topic ARN into the Lambda runtime
  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.clb_alerts.arn
    }
  }
  
  depends_on = [aws_iam_role_policy_attachment.lambda_vpc_access]
}

# Security Group for the Lambda Function
resource "aws_security_group" "lambda_sg" {
  name        = "clb-remediation-lambda-sg"
  description = "Security group for the remediation Lambda"
  vpc_id      = var.vpc_id # Replace with your VPC ID

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }
}

# Grant EventBridge permission to invoke the Lambda function
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.clb_remediation.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.clb_timeout_modification.arn
}

# Add the Lambda as the target to your previously created EventBridge rule
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.clb_timeout_modification.name
  target_id = "TriggerRemediationLambda"
  arn       = aws_lambda_function.clb_remediation.arn
}