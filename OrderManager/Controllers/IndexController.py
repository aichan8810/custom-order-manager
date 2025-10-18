from OrderManager.Services.CleaningTicketService import CleaningTicketService

class IndexController:
    def __init__(self):
        self.name = "IndexController"
    def index(self, data):
        if "tags" in data and "クリーニングチケット" in data["tags"]:
            cleaning_ticket_service = CleaningTicketService()
            return cleaning_ticket_service.sendApiRequest(data)
        return {"message": "No cleaning ticket found in tags"}
