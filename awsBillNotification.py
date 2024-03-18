import json
import boto3

def lambda_handler(event, context):
    # Initialize AWS services
    sns_client = boto3.client('sns')
    billing_client = boto3.client('ce')  # AWS Cost Explorer

    # Retrieve billing information
    response = billing_client.get_cost_and_usage(
        TimePeriod={
            'Start': '2024-01-01',
            'End': '2024-03-01'  # Modify the date range as needed
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']  # You can customize the metrics as needed
    )

    # Extract the total cost for the current billing period
    total_cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

    # Check if the bill is pending (total cost > 0)
    if total_cost > 0:
        # Send notification
        topic_arn = 'arn:aws:sns:ap-south-1:9*************:awsBillNotification'  # Replace with your SNS topic ARN
        message = f'Your AWS bill for the current month is pending. Total amount due: ${total_cost:.2f}'
        subject = 'Action Required: Your AWS Bill is Pending'

        sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )

        print('Billing notification sent successfully')
    else:
        print('No pending bills found')

    return {
        'statusCode': 200,
        'body': 'Billing notification process completed'
    }
