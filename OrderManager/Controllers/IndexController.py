from OrderManager.Services.CleaningTicketService import CleaningTicketService

class IndexController:
    def __init__(self):
        self.name = "IndexController"
    def index(self, data):
        if "tags" in data and "クリーニングチケット" in data["tags"]:
            cleaning_ticket_service = CleaningTicketService()
            order = cleaning_ticket_service.sendItemApiRequest(data)
            order_item = cleaning_ticket_service.sendOrderItemApiRequest(data)
        return {"message": "No cleaning ticket found in tags"}
