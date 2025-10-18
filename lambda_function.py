import json
import sys
import os

# Lambda関数のルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from OrderManager.Controllers.IndexController import IndexController

def lambda_handler(event, context):
    try:
        index_controller = IndexController()

        # イベント全体をログ出力（デバッグ用）
        print("Incoming Event:", json.dumps(event))

        # リクエストボディを取得
        body = event.get("body", "{}")

        # JSONとしてパース（失敗したら文字列のまま）
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {str(e)}")
            data = {"raw": body}

        print("✅ Received webhook:", json.dumps(data, ensure_ascii=False))

        # tagsに特定の値が含まれているかをチェック
        if "tags" in data and "クリーニングチケット" in data["tags"]:
            print("🎫 Cleaning ticket detected, processing...")
            result = index_controller.index(data)
            print("✅ Processing result:", json.dumps(result, ensure_ascii=False))

            # 結果にエラーが含まれているかチェック
            if isinstance(result, dict) and result.get("status") == "error":
                print(f"❌ Processing failed: {result.get('message', 'Unknown error')}")
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Processing failed", "details": result})
                }
        else:
            print("ℹ️ No cleaning ticket found in tags, skipping processing")

        # Shopify（またはcurl）へ 200 OK を返す
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"ok": True, "message": "Webhook processed successfully"})
        }

    except Exception as e:
        print(f"❌ Lambda handler error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error", "message": str(e)})
        }
