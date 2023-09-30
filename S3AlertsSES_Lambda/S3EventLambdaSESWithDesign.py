import json
import boto3
import os

ses_client = boto3.client('ses')

def send_email(bucket, key, recipient, event_type, sender_name, sender_email):
    sender = f'{sender_name} <{sender_email}>'
    subject = f'S3 Event Notification - {event_type}'
    body = f"""
        <html>
        <head>
        </head>
        <body style="text-align: left; font-family: Arial, sans-serif; color: black; background-color: #e3f2fd; padding: 5%">
            <h1 style="color: red; text-align: center">S3 Alert!</h1>
            <p>Hello {recipient},</p>
            <p>A {event_type} event occurred in the bucket {bucket}.</p>
            <p>File key: {key}</p>
        </body>
        </html>
    """
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
                'Html': {
                    'Data': body,
                },
            },
        }
    )
    print('Email sent to:', recipient)

def lambda_handler(event, context):
    recipients = ['user1@gmail.com', 'user2@gmail.com']
    sender_name = os.environ['SENDER_NAME']
    sender_email =  os.environ['SENDER_EMAIL']
    try:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            event_type = record['eventName']

            for recipient in recipients:
                send_email(bucket, key, recipient, event_type, sender_name, sender_email)
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
