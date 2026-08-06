variable "environment" { 
    type    = string 
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
