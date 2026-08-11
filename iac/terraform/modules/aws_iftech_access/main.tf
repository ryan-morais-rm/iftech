resource "aws_iam_user" "iftech_users" {
  for_each = toset([for i in range(1, 21) : "user-${var.environment}-${i}"])

  name = each.value

  tags = {
    Environment = "${var.environment}"
    UserTag     = each.value
  }
}

resource "aws_iam_group" "iftech_users_group" {
  name = "${var.environment}-users"
}

resource "aws_iam_group_membership" "iftech_users_membership" {
  name  = "${var.environment}-users-membership"
  group = aws_iam_group.iftech_users_group.name

  users = [for user in aws_iam_user.iftech_users : user.name]
}

resource "aws_iam_user_login_profile" "iftech_user_profiles" {
  for_each = aws_iam_user.iftech_users

  user                    = each.value.name
  password_reset_required = false
}

resource "aws_iam_group_policy_attachment" "iftech_readonly_attachments" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess",            
    "arn:aws:iam::aws:policy/AmazonVPCReadOnlyAccess",            
    "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",             
    "arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess",           
    "arn:aws:iam::aws:policy/ElasticLoadBalancingReadOnly",
    "arn:aws:iam::aws:policy/AutoScalingReadOnlyAccess"           
  ])

  group      = aws_iam_group.iftech_users_group.name
  policy_arn = each.value
}

resource "aws_iam_access_key" "iftech_user_keys" {
  for_each = aws_iam_user.iftech_users

  user = each.value.name
}

data "aws_s3_bucket" "existing_bucket" {
  bucket = "${var.environment}-${var.bucket_name}"
}

resource "aws_s3_object" "credentials_csv_s3" {
  bucket       = data.aws_s3_bucket.existing_bucket.id
  key          = "access_keys/guests_credentials.csv"
  content_type = "text/csv"

  content = "User,Password,AccessKeyId,SecretAccessKey\n${join("\n", [
    for k, user in aws_iam_user.iftech_users :
    "${user.name},${aws_iam_user_login_profile.iftech_user_profiles[k].password},${aws_iam_access_key.iftech_user_keys[k].id},${aws_iam_access_key.iftech_user_keys[k].secret}"
  ])}"
}