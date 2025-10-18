from OrderManager.Models.Order import Order
import uuid
from datetime import datetime

class CleaningTicketService:
    def __init__(self):
        self.name = "CleaningTicketService"

    def sendApiRequest(self, data):
        try:
            order = Order()

            # Shopifyデータから注文情報を取得
            order_name = data.get('name', 'Unknown Order')  # ルートレベルのname
            order_id = data.get('id', str(uuid.uuid4()))    # ルートレベルのid
            created_at = data.get('created_at', datetime.now().isoformat())  # ルートレベルのcreated_at

            print(f"🔍 Extracted data - Name: {order_name}, ID: {order_id}, Created: {created_at}")

            # 注文をDynamoDBに保存
            set_result = order.setOrder(
              order_id,
              order_name,
              created_at
            )
            
            print(f"✅ Order saved to DynamoDB: {set_result}")

            # 保存した注文を取得
            get_result = order.getOrder(order_id)
            print(f"✅ Order retrieved from DynamoDB: {get_result}")

            return {
                "status": "success",
                "order_id": order_id,
                "order_name": order_name,
                "created_at": created_at,
                "dynamodb_result": get_result
            }
        except Exception as e:
            print(f"❌ Error in CleaningTicketService: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
