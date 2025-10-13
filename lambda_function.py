def lambda_handler(event, context):
    print("Incoming Event:", json.dumps(event))
    body = event.get("body", "{}")
    data = json.loads(body)
    print("✅ Received webhook:", json.dumps(data))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"ok": True})
    }
