output "aws_console_login_url" {
  value       = "https://${data.aws_caller_identity.current.account_id}.signin.aws.amazon.com/console"
}

data "aws_caller_identity" "current" {}

output "credentials_s3_path" {
  value       = "s3://${data.aws_s3_bucket.existing_bucket.id}/${aws_s3_object.credentials_csv_s3.key}"
}