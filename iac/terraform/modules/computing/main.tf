resource "aws_key_pair" "iftech_key" {
  key_name   = "key-iftech-${var.environment}"
  public_key = file(var.ssh_public_key_path)
}

resource "aws_instance" "db_server" {
  ami                    = var.custom_db_ami_id
  instance_type          = "t3.small"
  subnet_id              = var.subnet_ids[0]
  vpc_security_group_ids = [var.ec2_security_group_id]
  key_name               = aws_key_pair.iftech_key.key_name  

  tags = {
    Name = "ec2-db-fixed-${var.environment}"
  }
}

resource "aws_lb" "alb" {
  name               = "alb-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]
  subnets            = var.subnet_ids

  tags = {
    Name = "alb-${var.environment}"
  }
}

resource "aws_lb_target_group" "tg" {
  name     = "tg-app-${var.environment}"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200-399"
    interval            = 15
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}

resource "aws_launch_template" "app_lt" {
  name_prefix   = "lt-app-${var.environment}-"
  image_id      = var.custom_ami_id
  instance_type = var.instance_type
  key_name      = aws_key_pair.iftech_key.key_name  

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [var.ec2_security_group_id]
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "ec2-asg-app-${var.environment}"
    }
  }
}

resource "aws_autoscaling_group" "asg" {
  name                = "asg-app-${var.environment}"
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.tg.arn]

  min_size         = 1
  desired_capacity = 1
  max_size         = 2

  launch_template {
    id      = aws_launch_template.app_lt.id
    version = "$Latest"
  }
}