from json import dumps
from time import time
from flask import request, jsonify
from hashlib import sha256
from datetime import datetime
from requests import get
from requests import post
import json
import os


class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        self.app = app
        self.openai_key = config["openai_key"]
        self.openai_api_base = config["openai_api_base"]
        self.routes = {
            "/backend-api/v2/conversation": {
                "function": self._conversation,
                "methods": ["POST"],
            }
        }

    def _conversation(self):
        try:
            message = request.json["content"]["message"]
            # url = f"{self.openai_api_base}/v1/chat/completions"
            # resp = post(
            #     url,
            #     headers={"Authorization": "Bearer %s" % self.openai_key},
            #     json={
            #         "model": "gpt-3.5-turbo",
            #         "messages": [{"role": "user", "content": "hello"}],
            #         "max_tokens": 50,
            #         "top_p": 1,
            #         "temperature": 0.5,
            #         "frequency_penalty": 0,
            #         "presence_penalty": 0,
            #         # "stream": True,
            #     },
            #     # stream=True,
            # )
            response_data = {"message": message, "success": True}
            return jsonify(response_data)

        except Exception as e:
            error_message = f"There was an error: {str(e)}"
            return jsonify({"message": error_message, "success": False}), 500
