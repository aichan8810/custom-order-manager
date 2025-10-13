import json

def lambda_handler(event, context):
    # イベント全体をログ出力（デバッグ用）
    print("Incoming Event:", json.dumps(event))

    # リクエストボディを取得
    body = event.get("body", "{}")

    # JSONとしてパース（失敗したら文字列のまま）
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        data = {"raw": body}

    print("✅ Received webhook:", json.dumps(data, ensure_ascii=False))

    # Shopify（またはcurl）へ 200 OK を返す
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"ok": True})
    }
