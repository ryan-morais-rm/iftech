from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import Route53, ELB
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users

with Diagram(
    "AWS Architecture - IFTech",
    filename="aws_architecture",
    show=False,
    direction="TB",
):

    users = Users("IFTech\nGuests")
    dns = Route53("Route 53")
    
    with Cluster("VPC"):
        alb = ELB("Application\nLoad Balancer")
        cloudwatch = Cloudwatch("CloudWatch\nAlarms (CPU / ALB Req)")

        with Cluster("Auto Scaling Group\n(Min: 1 | Max: 2)"):
            asg = AutoScaling("Scaling Policy")
            
            ec2_a = EC2("Instance A\nApp + AI Model")
            ec2_b = EC2("Instance B\nApp + AI Model")
            
            asg - [ec2_a, ec2_b]

    users >> dns >> alb >> ec2_a

    cloudwatch >> Edge(color="firebrick", style="dashed", label="Triggers Scaling") >> asg