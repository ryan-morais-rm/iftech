variable "aws_access_key" {
  description = "AWS AK"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS SK"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "admin_public_ip" {
  type        = string
}
