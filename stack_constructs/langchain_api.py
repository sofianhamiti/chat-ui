from constructs import Construct

from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration,
)


class API(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(
            self,
            "LambdaRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("apigateway.amazonaws.com"),
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSageMakerFullAccess"
                ),
            ],
        )

        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "apigateway:POST",
                    "apigateway:GET",
                    "apigateway:PUT",
                    "apigateway:DELETE",
                ],
                resources=["*"],
            )
        )

        # Create a Lambda function
        endpoint_handler = _lambda.DockerImageFunction(
            scope=self,
            id="LambdaFunction",
            function_name="endpoint-handler",
            role=role,
            code=_lambda.DockerImageCode.from_image_asset("langchain_lambda"),
            memory_size=1024,
            timeout=Duration.seconds(30),
        )
        # Create an API Gateway REST API
        api = apigw.LambdaRestApi(
            scope=self, id="EndpointAPI", handler=endpoint_handler
        )
        api.root.add_method("POST")
