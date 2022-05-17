import json
import boto3

#define variables: dynamodb as a boto3 resource, table_name as the DynamoDB table name, and table as the functional table resource
dynamodb = boto3.resource('dynamodb')
table_name = 'visitors'
table = dynamodb.Table(table_name)
#set primary key to ID 0
ID = '0'



def lambda_handler(event, context):
#Set action message for logs
    print('Fetching Item ID = {} from the DB\n'.format(ID))
     
    response = table.get_item(
        Key={
            'ID': ID
        }
        )
    if 'Item' in response: #if response includes Item data, perform update to increase visitor count
        response = table.update_item(
             Key={
                'ID': ID
            },
            UpdateExpression="set total_count = total_count + :N",
            ExpressionAttributeValues={
                ':N': 1
            }
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('Item updated with status = {} OK'.format(response['ResponseMetadata']['HTTPStatusCode']))
        else:
            print('An error occurred while updating the item from the DB') #error message if bad response from DB
    else:
        print('Item ID = {} could not be found in the DB'.format(ID)) #error message if item can't be found
#CORS response
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        }
    }