output "alb_dns_name" {
  value       = aws_lb.alb.dns_name
  description = "URL que os participantes vão acessar no navegador"
}

output "db_private_ip" {
  value       = aws_instance.db_server.private_ip
  description = "IP Privado do Banco para apontar na aplicação"
}

output "db_public_ip" {
  value       = aws_instance.db_server.public_ip
  description = "IP Público da instância de banco para acesso Ansible/SSH"
}