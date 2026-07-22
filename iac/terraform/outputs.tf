output "url_app" {
  value       = "http://${module.computing.alb_dns_name}"
  description = "LLM app url"
}