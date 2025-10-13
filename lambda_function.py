import json
import Services.OrderManager.Controllers.IndexController as IndexController
def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    index_controller = IndexController()
    index_controller.index()
    return {
        'statusCode': 200,
        'body': json.dumps({'message': IndexController.index()})
    }
