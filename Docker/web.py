from flask import Flask
import boto3
import json

queue_name='testofguruprasad'

def sqs_create_queue(queue_name):
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.create_queue(
        QueueName=queue_name,
        Attributes={
            "DelaySeconds": "2",
            "VisibilityTimeout": "30",
        }
    )
    print(response)
    return response

def sqs_send_message(queue_url):
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    message= {"Message": "Hi"}
    response = sqs_client.send_message(
         QueueUrl=queue_url,
         MessageBody=json.dumps(message)
    )
    print(response)
    return response

def sqs_get_url(queue_name):
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.get_queue_url(
        QueueName=queue_name,
    )
    return response["QueueUrl"]

def sqs_receive_message(queue_url):
    processed_msg_count=0
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=2,
        WaitTimeSeconds=20,
    )
    print(f"Count of messages received: {len(response.get('Messages', []))}")
    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {json.loads(message_body)}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")
        receipt_handle=message['ReceiptHandle']
        print('*'*60)
        print('Hello World')
        processed_msg_count+=1
        print('*'*60)
        sqs_delete_message(queue_url,receipt_handle)
    return processed_msg_count


def sqs_delete_message(queue_url,receipt_handle):
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle,
    )
    print(response)

def print_message(processed_msg_count):
    a=''
    for i in range(0,processed_msg_count):
        a= a + '</br>' 'Hello world'
    print(a)
    return a

# Flask configuration    

app = Flask(__name__)

@app.route('/hello')
def helloIndex():
    print('Main code starts here')
    return 'hello world'

@app.route('/createqueue')
def createqueueIndex():
    print('Main code starts here')  
    response=sqs_create_queue(queue_name)
    queue_url=response.get('QueueUrl')
    return 'Queue created with url:' + ' ' + queue_url

@app.route('/sendmessage')
def sendmessageIndex():
    queue_url=sqs_get_url(queue_name)
    response=sqs_send_message(queue_url)   
    return response

@app.route('/receivemessage')
def receivemessageIndex():
    queue_url=sqs_get_url(queue_name)
    processed_msg_count=sqs_receive_message(queue_url)  
    return print_message(processed_msg_count)
    
app.run(host='0.0.0.0', port=5000)