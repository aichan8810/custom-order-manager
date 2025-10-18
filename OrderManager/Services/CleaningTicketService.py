from OrderManager.Models.Order import Order
import uuid

class CleaningTicketService:
    def __init__(self):
        self.name = "CleaningTicketService"

    def sendApiRequest(self, data):
        try:
            order = Order()
            # データから注文名を取得（適切なキーに修正）
            order_name = data.get('data', {}).get('name', 'Unknown Order')
            order_id = data.get('order_id', str(uuid.uuid4()))

            # 注文をDynamoDBに保存
            set_result = order.setOrder(order_id, order_name)
            print(f"✅ Order saved to DynamoDB: {set_result}")

            # 保存した注文を取得
            get_result = order.getOrder(order_id)
            print(f"✅ Order retrieved from DynamoDB: {get_result}")

            return {
                "status": "success",
                "order_id": order_id,
                "order_name": order_name,
                "dynamodb_result": get_result
            }
        except Exception as e:
            print(f"❌ Error in CleaningTicketService: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
