# 1. Create the SNS Topic
resource "aws_sns_topic" "clb_alerts" {
  name = "clb-timeout-alerts"
}

# 2. Subscribe an email address to the SNS Topic
resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.clb_alerts.arn
  protocol  = "email"
  endpoint  = "" # Replace with your actual email address
}

# 3. Allow the Lambda Function to Publish to the SNS Topic
resource "aws_iam_role_policy" "lambda_sns_publish_policy" {
  name = "clb-timeout-sns-publish-policy"
  role = aws_iam_role.lambda_remediation_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "sns:Publish"
        Resource = aws_sns_topic.clb_alerts.arn
      }
    ]
  })
}