import json

def lambda_handler(event, context):
    print("Incoming Event:", json.dumps(event))
    try:
        body = json.loads(event["body"])
        print("Shopify webhook payload:", json.dumps(body, indent=2))
        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True})
        }
    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 400, "body": str(e)}
