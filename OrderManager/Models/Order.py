
"""
order_t
  id: string
  order_id: string
"""
import json
import boto3
import os
import uuid
class Order:
    def setOrder(self, order_id, order_name):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      item = {
          'id': order_id,  # order_idをプライマリキーとして使用
          'order_name': order_name,
          'created_at': str(uuid.uuid4()),  # 一意のタイムスタンプとして使用
          'status': 'created'
      }
      response = table.put_item(Item=item)
      print(f"✅ DynamoDB put_item response: {response}")
      return response

    def getOrder(self, order_id):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      try:
          response = table.get_item(Key={'id': order_id})
          if 'Item' in response:
              return response['Item']
          else:
              return {"error": "Order not found"}
      except Exception as e:
          print(f"❌ Error getting order: {str(e)}")
          return {"error": str(e)}
    def updateOrder(self, order_id, data):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      response = table.update_item(Key={'id': order_id}, UpdateExpression='set #data = :data', ExpressionAttributeNames={'#data': 'data'}, ExpressionAttributeValues={':data': data})
      return response
    def deleteOrder(self, order_id):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      response = table.delete_item(Key={'id': order_id})
      return response
