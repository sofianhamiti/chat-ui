from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns,
    Duration,
)


class FrontEndService(Construct):
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        # ==============================
        # ======= CFN PARAMETERS =======
        # ==============================
        port = 8880
        name = "chatbot"

        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        role = iam.Role(
            scope=self,
            id="TASKROLE",
            assumed_by=iam.ServicePrincipal(service="ecs-tasks.amazonaws.com"),
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess")
        )

        # ==================================================
        # ==================== VPC =========================
        # ==================================================
        vpc = ec2.Vpc(self, "vpc", max_azs=2)

        # ==================================================
        # =============== FARGATE SERVICE ==================
        # ==================================================
        cluster = ecs.Cluster(scope=self, id="cluster", cluster_name=name, vpc=vpc)

        task_definition = ecs.FargateTaskDefinition(
            scope=self,
            id="taskdefinition",
            task_role=role,
            cpu=4 * 1024,
            memory_limit_mib=8 * 1024,
        )

        container = task_definition.add_container(
            id="Container",
            image=ecs.ContainerImage.from_asset(directory="frontend"),
            logging=ecs.LogDriver.aws_logs(stream_prefix=name),
        )
        port_mapping = ecs.PortMapping(
            container_port=port, host_port=port, protocol=ecs.Protocol.TCP
        )
        container.add_port_mappings(port_mapping)

        self.fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(
            scope=self,
            id="service",
            service_name=name,
            cluster=cluster,
            task_definition=task_definition,
        )

        # Setup security group
        self.fargate_service.service.connections.security_groups[0].add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(port),
            description="Allow inbound from VPC for chatui",
        )

        # Setup autoscaling policy
        scaling = self.fargate_service.service.auto_scale_task_count(max_capacity=2)
        scaling.scale_on_cpu_utilization(
            id="autoscaling",
            target_utilization_percent=70,
            scale_in_cooldown=Duration.seconds(60),
            scale_out_cooldown=Duration.seconds(60),
        )
