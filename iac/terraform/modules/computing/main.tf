resource "aws_key_pair" "iftech_key" {
  key_name   = "key-iftech-${var.environment}"
  public_key = file(var.ssh_public_key_path)
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
  port     = 8501
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path                = "/_stcore/health"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 15
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
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

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_size           = 50
      volume_type           = "gp3"
      delete_on_termination = true
    }
  }

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

  health_check_type         = "ELB"
  health_check_grace_period = 600

  launch_template {
    id      = aws_launch_template.app_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "ec2-asg-app-${var.environment}"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "cpu_policy" {
  name                      = "target-tracking-cpu-${var.environment}"
  autoscaling_group_name    = aws_autoscaling_group.asg.name
  policy_type               = "TargetTrackingScaling"
  estimated_instance_warmup = 300


  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }

    target_value = 70.0
  }
}

resource "aws_autoscaling_policy" "alb_requests_policy" {
  name                      = "target-tracking-alb-requests-${var.environment}"
  autoscaling_group_name    = aws_autoscaling_group.asg.name
  policy_type               = "TargetTrackingScaling"
  estimated_instance_warmup = 300

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = "${aws_lb.alb.arn_suffix}/${aws_lb_target_group.tg.arn_suffix}"
    }

    target_value = 100.0
  }
}