from constructs import Construct
from aws_cdk import App, Stack, CfnOutput
from stack_constructs.langchain_api import API
from stack_constructs.frontend_service import FrontEndService


class ChatBotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        # ==================================================
        # ================== PARAMETERS ====================
        # ==================================================
        port = 8880
        name = "chatbot"
        endpoint_name = "j2-jumbo-instruct"

        # ==================================================
        # =============== FrontEnd SERVICE =================
        # ==================================================
        ui_service = FrontEndService(self, "FrontEndService")

        # ==================================================
        # ===================== API ========================
        # ==================================================
        api = API(self, "API")

        # ==================================================
        # =================== OUTPUTS ======================
        # ==================================================
        CfnOutput(
            scope=self,
            id="LoadBalancerDNS",
            value=ui_service.fargate_service.load_balancer.load_balancer_dns_name,
        )


app = App()
ChatBotStack(app, "ChatBotStack")
app.synth()
