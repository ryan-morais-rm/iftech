variable "environment" { 
    type    = string 
}

variable "custom_ami_id" {
  type        = string
  description = "ID from customized AMI with docker + LLM model + ansible configs..."
}

variable "tfstate_bucket_name" {
  type      = string
  sensitive = true 
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "admin_public_ip" {
  type        = string
}
