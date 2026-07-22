variable "environment" { 
    type = string 
    default = "iftech" 
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
  default   = "ami-0123456789abcdef0" # Only for demo, not a real AMI
}
variable "instance_type" { 
    type = string 
    default = "t3.medium" 
}
variable "ssh_public_key_path" {
  type        = string
  default     = "~/.ssh/id_iftech.pub"
  description = "SSH pub key"
}