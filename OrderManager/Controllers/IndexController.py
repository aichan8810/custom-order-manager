from OrderManager.Services.CleaningTicketService import CleaningTicketService

class IndexController:
    def __init__(self):
        self.name = "IndexController"
    def index(self, data):
        if "tags" in data and "クリーニングチケット" in data["tags"]:
            cleaning_ticket_service = CleaningTicketService()

            # 注文をorder_tに保存
            order_result = cleaning_ticket_service.sendApiRequest(data)
            print(f"✅ Order result: {order_result}")

            # 注文アイテムをorder_item_tに保存
            order_item_result = cleaning_ticket_service.sendItemApiRequest(data)
            print(f"✅ Order item result: {order_item_result}")

            return {
                "order_result": order_result,
                "order_item_result": order_item_result
            }
        return {"message": "No cleaning ticket found in tags"}
