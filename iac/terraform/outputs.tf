output "url_app" {
  value       = "http://${module.computing.alb_dns_name}"
  description = "LLM app url"
}

output "db_server_ip" {
  value       = module.computing.db_public_ip
  description = "DB IP address"
}