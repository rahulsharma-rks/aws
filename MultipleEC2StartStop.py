import boto3

# Initialize the EC2 client
ec2_client = boto3.client('ec2')

# List of instance IDs to manage
INSTANCE_IDS = ['i-0cf458e5280ca9b61', 'i-013c55385b5db4c5b','i-024f1229802ff56ac']

def lambda_handler(event, context):
    try:
        # Describe the instances to get their current states
        response = ec2_client.describe_instances(InstanceIds=INSTANCE_IDS)
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                
                if state == 'running':
                    # If the instance is running, stop it
                    print(f"Stopping instance {instance_id}")
                    ec2_client.stop_instances(InstanceIds=[instance_id])
                elif state == 'stopped':
                    # If the instance is stopped, start it
                    print(f"Starting instance {instance_id}")
                    ec2_client.start_instances(InstanceIds=[instance_id])
                else:
                    print(f"Instance {instance_id} is in {state} state; no action taken.")
                    
        return {
            'statusCode': 200,
            'body': 'Successfully toggled instance states.'
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
