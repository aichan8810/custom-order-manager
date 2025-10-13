import json, os, hmac, hashlib, base64

def verify_webhook(headers, body):
    secret = os.environ.get("SHOPIFY_WEBHOOK_SECRET", "")
    hmac_header = headers.get("X-Shopify-Hmac-Sha256", "")
    digest = base64.b64encode(
        hmac.new(secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    )
    return hmac.compare_digest(digest, hmac_header.encode("utf-8"))

def lambda_handler(event, context):
    headers = event.get("headers", {}) or {}
    body = event.get("body", "{}")

    print("Incoming Event:", json.dumps(event))

    # 署名チェック（テスト実行時はスキップ）
    if headers and os.environ.get("SHOPIFY_WEBHOOK_SECRET"):
        if not verify_webhook(headers, body):
            print("❌ Invalid webhook signature")
            return {"statusCode": 401, "body": "Unauthorized"}

    data = json.loads(body)
    print("✅ Received webhook:", json.dumps(data))
    return {"statusCode": 200, "body": json.dumps({"ok": True})}
