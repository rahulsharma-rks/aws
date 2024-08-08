import boto3
from datetime import datetime

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Update with your instance ID
    instance_id = 'i-0cf458e5280ca9b61'  

    # Describe the instance to get its volumes
    response = ec2.describe_instances(InstanceIds=[instance_id])
    volumes = [volume['Ebs']['VolumeId'] for reservation in response['Reservations'] for instance in reservation['Instances'] for volume in instance['BlockDeviceMappings']]
    
    snapshot_ids = []
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Create a snapshot for each volume
    for volume_id in volumes:
        snapshot = ec2.create_snapshot(VolumeId=volume_id, Description='Daily snapshot')
        snapshot_ids.append(snapshot['SnapshotId'])
    
    # Prepare the message
    message = f"Timestamp: {timestamp}\n"
    message += f"Instance ID: {instance_id}\n"
    message += "Snapshot IDs: " + ", ".join(snapshot_ids)
    
    # Send the notification
    sns.publish(
        TopicArn='arn:aws:sns:ap-south-1:965519929135:EBSBackupNotification',  
        Subject='Daily EBS Snapshot Completed',
        Message=message
    )
