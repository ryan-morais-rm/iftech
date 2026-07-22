output "alb_dns_name" {
  value       = aws_lb.alb.dns_name
  description = "Guests are going to use this URL to acess the application"
}