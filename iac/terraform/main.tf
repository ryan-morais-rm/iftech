module "network" {
  source          = "./modules/network"
  environment     = var.environment
  admin_public_ip = var.admin_public_ip
}

module "computing" {
  source                = "./modules/computing"
  environment           = var.environment
  vpc_id                = module.network.vpc_id
  subnet_ids            = module.network.public_subnet_ids
  alb_security_group_id = module.network.alb_security_group_id
  ec2_security_group_id = module.network.ec2_security_group_id

  depends_on = [
    module.network
  ]
}

module "bucket" {
  source      = "./modules/bucket"
  environment = var.environment
}