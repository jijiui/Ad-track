from __future__ import print_function
import json
import boto3
import time
from boto3 import dynamodb
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from decimal import *
import urllib
import json
#Why the Primary Key is "Date & Time" and range key is "M-Phone ID"? Beacause the rule is that if these two keys of two items are the same, one of them will be deleted 
print('Loading function')

def lambda_handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    operation = event['operation']

    if 'tableName' in event:
        dynamo = boto3.resource('dynamodb').Table(event['tableName'])

    operations = {
        'create': lambda x: dynamo.put_item(**x),
        'read': lambda x: dynamo.get_item(**x),
        'echo': lambda x: x,
        'ping': lambda x: 'pong',
        'check': lambda x: dynamo.query(**x)
    }

    
    if operation in operations:
        return operations[operation](event.get('payload'))
    else:
       raise ValueError('Unrecognized operation "{}"'.format(operation))
