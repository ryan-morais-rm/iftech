variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}
variable "environment" {
  type    = string
  default = "iftech"
}
variable "admin_public_ip" {
  type        = string
  description = "Admin public IP from root module"
}