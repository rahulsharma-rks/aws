import json
import boto3

ses_client = boto3.client('ses')

def send_email(bucket, key, recipient, event_type):
    sender = 'sender@gmail.com'  
    subject = f'S3 Event Notification - {event_type}'
    body = f'Hello {recipient},\n\nA {event_type} event occurred in the bucket {bucket}.\nFile key: {key}'

    response = ses_client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [recipient],
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': body,
                },
            },
        }
    )

    print('Email sent to:', recipient)

def lambda_handler(event, context):
    recipients = ['user1@gmail.com', 'user2@gmail.com'] 

    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            event_type = record['eventName']

            for recipient in recipients:
                send_email(bucket, key, recipient, event_type)
                
        return {
            'statusCode': 200,
            'body': json.dumps('Emails sent successfully')
        }
    except Exception as e:
        print('Error sending emails:', e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending emails')
        }
