"""
Replicate data from primary bucket to backup bucket, when new file is uploaded in primary bucket, it should automatically reflect in 
backup bucket. Data should not be deleted from backup bucket even its deleted from primary bucket.
"""


import boto3
import urllib.parse

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        source_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        destination_bucket = 'backup-bucket-7'
        copy_source = {'Bucket': source_bucket, 'Key': source_key}

        try:
            # Copy the object to the backup bucket
            s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=source_key)
            print(f'Successfully copied {source_key} from {source_bucket} to {destination_bucket}')
            
            # Send SNS notification
            sns.publish(
                TopicArn='arn:aws:sns:ap-south-1:965519929135:s3DataBackUpSNS',
                Subject='File Uploaded to Backup Bucket',
                Message=f'The file {source_key} has been successfully uploaded to {destination_bucket}.'
            )
            print(f'Successfully sent SNS notification for {source_key}')
        except Exception as e:
            print(f'Error copying {source_key} from {source_bucket} to {destination_bucket}: {str(e)}')
            raise e
