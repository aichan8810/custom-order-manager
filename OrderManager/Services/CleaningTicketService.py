from OrderManager.Models.Order import Order
import uuid
from datetime import datetime

class CleaningTicketService:
    def __init__(self):
        self.name = "CleaningTicketService"

    def sendApiRequest(self, data):
        try:
            order = Order()

            # line_itemsを処理して必要な情報のみを抽出
            line_items = []
            for item in data.get('line_items', []):
                line_item = {
                    'product_id': item.get('product_id'),
                    'title': item.get('title'),
                    'variant_title': item.get('variant_title'),
                    'quantity': item.get('quantity'),
                    'price': item.get('price'),
                    'gift_card': item.get('gift_card', False)
                }
                line_items.append(line_item)

            # 指定された形式で注文データを構築
            order_data = {
                'order_id': str(data.get('id', '')),
                'order_number': data.get('order_number'),
                'tags': data.get('tags', ''),
                'financial_status': data.get('financial_status'),
                'fulfillment_status': data.get('fulfillment_status'),
                'cancel_reason': data.get('cancel_reason'),
                'total_price': data.get('total_price', ''),
                'currency': data.get('currency', ''),
                'created_at': data.get('created_at', ''),
                'updated_at': data.get('updated_at', ''),
                'customer_email': data.get('email', ''),
                'customer_locale': data.get('customer_locale', ''),
                'browser_ip': data.get('browser_ip', ''),
                'line_items': line_items
            }

            print(f"🔍 Extracted order data: {order_data}")

            # 注文をDynamoDBに保存
            set_result = order.setOrder(order_data)
            print(f"✅ Order saved to DynamoDB: {set_result}")

            # 保存した注文を取得
            get_result = order.getOrder(order_data['order_id'])
            print(f"✅ Order retrieved from DynamoDB: {get_result}")

            return {
                "status": "success",
                "order_id": order_data['order_id'],
                "order_number": order_data['order_number'],
                "dynamodb_result": get_result
            }
        except Exception as e:
            print(f"❌ Error in CleaningTicketService: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
