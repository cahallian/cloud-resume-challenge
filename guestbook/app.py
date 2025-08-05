import os
import json
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    # Handle preflight CORS
    if event.get('httpMethod', '') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({'message': 'CORS preflight'})
        }

    body = json.loads(event['body'])
    name = body.get('name', '')
    role = body.get('role', '')

    if not name:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Name is required.'})
        }
    if not role:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Role is required.'})
        }
    if len(name) > 25:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Name must be 25 characters or fewer.'})
        }
    if len(role) > 25:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Role must be 25 characters or fewer.'})
        }

    # Check for duplicate (name + role)
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('name').eq(name) & boto3.dynamodb.conditions.Attr('role').eq(role)
    )
    if response['Items']:
        return {
            'statusCode': 409,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Duplicate entry: this name and role already exist.'})
        }

    entry = {
        'id': str(uuid.uuid4()),
        'name': name,
        'role': role,
        'visitorNumber': body.get('visitorNumber', ''),
    }
    table.put_item(Item=entry)
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'message': 'Guestbook entry added'})
    }