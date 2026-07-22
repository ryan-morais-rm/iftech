module "network" {
  source          = "./modules/network"
  environment     = "iftech"
  admin_public_ip = var.admin_public_ip
}

module "computing" {
  source                = "./modules/computing"
  environment           = "iftech"
  vpc_id                = module.network.vpc_id
  subnet_ids            = module.network.public_subnet_ids
  alb_security_group_id = module.network.alb_security_group_id
  ec2_security_group_id = module.network.ec2_security_group_id
}