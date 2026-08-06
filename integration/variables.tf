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
}

variable "bucket_name" {
  type        = string
  sensitive   = true
}

variable "environment" {
    type = string
}

variable "repository" {
    type = string
}