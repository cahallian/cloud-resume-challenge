import os
import json
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    body = json.loads(event['body'])
    entry = {
        'id': str(uuid.uuid4()),
        'name': body.get('name', ''),
        'role': body.get('role', ''),
        'visitorNumber': body.get('visitorNumber', ''),
    }
    table.put_item(Item=entry)
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'Entry added'})
    }