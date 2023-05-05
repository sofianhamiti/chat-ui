from requests import post
from flask import request, jsonify


class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        self.app = app
        self.api_url = config["api_url"]
        self.routes = {
            "/backend-api": {
                "function": self._conversation,
                "methods": ["POST"],
            }
        }

    def _conversation(self):
        try:
            message = request.json["content"]["message"]
            resp = post(
                self.api_url,
                # headers={},
                json={
                    "prompt": message,
                },
            )
            print(resp)
            return jsonify({"message": message, "success": True})

        except Exception as e:
            error_message = f"There was an error: {str(e)}"
            return jsonify({"message": error_message, "success": False}), 500
