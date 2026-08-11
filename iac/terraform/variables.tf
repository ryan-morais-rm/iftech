variable "environment" { 
    type    = string 
}

variable "custom_ami_id" {
  type        = string
}

variable "tfstate_bucket_name" {
  type      = string
  sensitive = true 
}

variable "aws_region" {
  type        = string
}

variable "admin_public_ip" {
  type        = string
  sensitive   = true 
}
