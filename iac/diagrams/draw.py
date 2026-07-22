from diagrams import Diagram, Cluster
from diagrams.aws.network import Route53, ELB
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.onprem.client import Users

with Diagram(
    "AWS Architecture",
    filename="aws_architecture",
    show=False,
    direction="TB",
):

    users = Users("IFTech GUESTS")

    dns = Route53("Elastic IP\nRoute 53")

    alb = ELB("Application\nLoad Balancer")

    with Cluster("VPC"):

        with Cluster("AS Group\nMin:1 | Desired:1 | Max:2"):

            asg = AutoScaling("Auto Scaling")

            ec2_a = EC2("Instance A\nApp Web\nLLM Server")

            ec2_b = EC2("Instance B\nApp Web\nLLM Server")

            asg >> [ec2_a, ec2_b]

    users >> dns >> alb >> asg