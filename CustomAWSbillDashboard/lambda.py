import boto3
import json
import datetime

def lambda_handler(event, context):
    # Set up AWS Cost Explorer client
    cost_explorer = boto3.client('ce')

    # Get the current date and one day before for filtering the cost data
    end_date = datetime.datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=1)

    # Fetch cost data from AWS Cost Explorer
    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost']
    )

    # Store the cost data in S3
    s3_bucket_name = 'buckteName'
    s3_key = f'cost_data/{end_date.strftime("%Y-%m-%d")}.json'
    s3 = boto3.client('s3')
    s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=json.dumps(response))

    return {
        'statusCode': 200,
        'body': json.dumps('Cost data successfully collected and stored.')
    }
