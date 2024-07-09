import json
import boto3
import os


def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    instance_id = os.environ['INSTANCE_ID']
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    
    # Determine the action based on the rule name
    if 'rule_name' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing rule_name in event')
        }
    
    rule_name = event['rule_name']
    
    if rule_name == 'StartInstanceRule':
        response = ec2.start_instances(InstanceIds=[instance_id])
        action = 'started'
        subject = 'EC2 Instance Started'
        message = f'Your EC2 instance {instance_id} has been started.'
    elif rule_name == 'StopInstanceRule':
        response = ec2.stop_instances(InstanceIds=[instance_id])
        action = 'stopped'
        subject = 'EC2 Instance Stopped'
        message = f'Your EC2 instance {instance_id} has been stopped.'
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid rule name')
        }
    
    # Send email notification
    sns.publish(
        TopicArn=sns_topic_arn,
        Subject=subject,
        Message=message
    )
    """
    #List Instances in all Region.
    ec2Region = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in ec2Region:
        instanceDetails = []
        ec2Client = boto3.client('ec2', region_name = region, aws_access_key_id = os.environ['accessKey'], aws_secret_access_key = os.environ['secretKey'])
        
        response = ec2Client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                inst_dict = {
                    'instance_id': instance["InstanceId"],
                    'instance_type' : instance["InstanceType"],
                    'private_ip': instance["PrivateIpAddress"], 
                    'monitoring' : instance["Monitoring"]["State"],
                    'location' : instance["Placement"]["AvailabilityZone"]
                }
            for sg in instance["SecurityGroups"]:
                sg_dict = {
                    'security_group' : sg["GroupId"]
                }
                print(sg_dict)
            print(inst_dict)
            print("------------*****------------------")
        """
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
