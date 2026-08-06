resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

resource "aws_iam_role" "github_actions_role" {
  name = "GitHubActionsTerraformRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.repository}:*"
          }
        }
      }
    ]
  })
}

data "aws_iam_policy_document" "github_actions_policy" {
  statement {
    effect = "Allow"
    actions = [
      "ec2:*",                  
      "elasticloadbalancing:*", 
      "autoscaling:*",          
      "cloudwatch:*",           
      "logs:*",                 
      "s3:*",                   
      
      "iam:CreateServiceLinkedRole", 
      "iam:PassRole",                
      "iam:GetRole",
      "iam:ListInstanceProfiles"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "github_actions_restricted" {
  name        = "GitHubActionsTerraformRestricted"
  description = "Permissoes restritas para o pipeline de CI/CD do GitHub Actions"
  policy      = data.aws_iam_policy_document.github_actions_policy.json
}

resource "aws_iam_role_policy_attachment" "terraform_restricted_access" {
  role       = aws_iam_role.github_actions_role.name
  policy_arn = aws_iam_policy.github_actions_restricted.arn
}