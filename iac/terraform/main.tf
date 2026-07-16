resource "aws_vpc" "vpc_teste" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "vpc-teste-iftech"
  }
}

resource "aws_subnet" "subnet_teste" {
  vpc_id                  = aws_vpc.vpc_teste.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "subnet-teste-iftech"
  }
}

output "vpc_id" {
  value       = aws_vpc.vpc_teste.id
  description = "ID da VPC criada na AWS"
}