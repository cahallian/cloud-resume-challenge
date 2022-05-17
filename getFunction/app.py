import simplejson as json
import boto3

#define variables: dynamodb as a boto3 resource, table_name as the DynamoDB table name, and table as the functional table resource
dynamodb = boto3.resource('dynamodb')
table_name = 'visitors'
table = dynamodb.Table(table_name)
#set primary key
ID = '0'


def lambda_handler(event, context):
    print('Fetching Item ID = {} from the DB\n'.format(ID)) #Set action message for logs
    
    response = table.get_item( #get data from DB
        Key={
            'ID': ID
        }
    )
        
    if 'Item' in response:
        return {
            "statusCode": 200,
            'headers': {
                        'Access-Control-Allow-Headers': '*', #CORS Response
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': '*'
            },
            "body": json.dumps({"counter": response['Item'].get('total_count'), #String message for HTML pickup
            }),
        }
    else:
            print('Item ID = {} not found in the DB'.format(id)) #error message if attribute can't be found