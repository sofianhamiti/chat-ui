import json
import ai21

ENDPOINT_NAME = "j2-jumbo-instruct"


def query_endpoint(input_text, endpoint_name):
    response = ai21.Completion.execute(
        sm_endpoint=endpoint_name,
        prompt=input_text,
        maxTokens=200,
        temperature=0.7,
        numResults=1,
    )
    return response["completions"][0]["data"]["text"]


def lambda_handler(event, context):
    print(json.dumps(event))
    event_body = json.loads(event["body"])

    try:
        text_response = query_endpoint(
            input_text=event_body["prompt"],
            endpoint_name=ENDPOINT_NAME,
        )
        return {"statusCode": 200, "body": text_response}

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": str(e)}
