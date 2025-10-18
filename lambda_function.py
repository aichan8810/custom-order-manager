import json
import sys
import os

# Lambda関数のルートディレクトリをPythonパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# デバッグ用：パスをログ出力
print(f"Python path: {sys.path}")
print(f"Current directory: {current_dir}")
print(f"Files in current directory: {os.listdir(current_dir)}")

try:
    from OrderManager.Controllers.IndexController import IndexController
    print("✅ IndexController imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # フォールバック：相対インポートを試す
    try:
        from .OrderManager.Controllers.IndexController import IndexController
        print("✅ IndexController imported with relative import")
    except ImportError as e2:
        print(f"❌ Relative import also failed: {e2}")
        raise e

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

            # JSONシリアライゼーション用のヘルパー関数
            def json_serializer(obj):
                if hasattr(obj, 'to_integral_value'):  # Decimal型のチェック
                    return int(obj)
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

            try:
                print("✅ Processing result:", json.dumps(result, ensure_ascii=False, default=json_serializer))
            except Exception as e:
                print(f"❌ JSON serialization error: {e}")
                print("Raw result:", result)

            # 結果にエラーが含まれているかチェック
            if isinstance(result, dict) and result.get("status") == "error":
                print(f"❌ Processing failed: {result.get('message', 'Unknown error')}")
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Processing failed", "details": result}, default=json_serializer)
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
