import json


def lambda_handler(event, context):

    print("HELLO FROM MINIMAL LAMBDA")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "minimal lambda works"
        })
    }