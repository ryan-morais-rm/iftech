variable "environment" {
  type    = string
}
variable "vpc_id" { 
    type = string 
}
variable "subnet_ids" { 
    type = list(string) 
}
variable "ec2_security_group_id" { 
    type = string 
}
variable "alb_security_group_id" { 
    type = string 
}
variable "custom_ami_id" {
  type        = string
  description = "ID from customized AMI with docker + LLM model + ansible configs..."
}
variable "instance_type" { 
    type = string 
    default = "c5.xlarge" 
}
variable "ssh_public_key_path" {
  type        = string
  default     = "~/.ssh/id_iftech.pub"
  description = "SSH pub key"
}