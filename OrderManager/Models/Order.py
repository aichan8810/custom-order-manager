"""
order_t
  id: string
  order_id: string
"""
import json
import boto3
import os
import uuid
from datetime import datetime

class Order:
    def setOrder(self, order_id, order_name, created_at):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      item = {
          'com': str(uuid.uuid4()),  # 'com'キーを直接使用
          'order_id': order_id,      # order_idも保存
          'order_name': order_name,
          'created_at': created_at,
          'status': 'created'
      }
      print(f"🔍 Putting item with key 'com': {item['com']}, order_id: {order_id}")
      response = table.put_item(Item=item)
      print(f"✅ DynamoDB put_item response: {response}")
      return response

    def getOrder(self, order_id):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      try:
          # order_idで検索するために、comキーの値を取得する必要がある
          # 現在の実装では、comキーにUUIDが設定されているため、
          # 直接order_idで検索することはできない
          # 代わりに、Scan操作でorder_idを含むアイテムを検索
          response = table.scan(
              FilterExpression='order_id = :order_id',
              ExpressionAttributeValues={':order_id': order_id}
          )

          if response['Items']:
              return response['Items'][0]  # 最初のマッチしたアイテムを返す
          else:
              return {"error": "Order not found"}
      except Exception as e:
          print(f"❌ Error getting order: {str(e)}")
          return {"error": str(e)}
    def updateOrder(self, order_id, data):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      response = table.update_item(Key={'com': order_id}, UpdateExpression='set #data = :data', ExpressionAttributeNames={'#data': 'data'}, ExpressionAttributeValues={':data': data})
      return response
    def deleteOrder(self, order_id):
      dynamoDb = boto3.resource('dynamodb')
      table = dynamoDb.Table('order_t')
      response = table.delete_item(Key={'com': order_id})
      return response
