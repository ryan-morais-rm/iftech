module "bucket" {
  source = "./modules/bucket"
  bucket_name = var.bucket_name
  environment = var.environment
}

module "iam" {
  source = "./modules/iam"
  repository  = var.repository
}