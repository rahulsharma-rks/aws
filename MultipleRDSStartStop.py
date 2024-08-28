'''
Note for RDS:
Not all RDS instance types support stopping and starting. For example, Aurora clusters don't support stopping, but individual Aurora instances do.
Stopping and starting are typically supported for Single-AZ DB instances and require that the instance is not in a Multi-AZ configuration.
'''

import boto3

# Initialize the RDS client
rds_client = boto3.client('rds')

# List of RDS instance identifiers to manage
DB_INSTANCE_IDENTIFIERS = ['database-1', 'database-2-postgres']

def lambda_handler(event, context):
    try:
        for db_instance_id in DB_INSTANCE_IDENTIFIERS:
            # Describe the instance to get its current state
            response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
            db_instance_status = response['DBInstances'][0]['DBInstanceStatus']
            
            if db_instance_status == 'available':
                # If the instance is running, stop it
                print(f"Stopping RDS instance {db_instance_id}")
                rds_client.stop_db_instance(DBInstanceIdentifier=db_instance_id)
            elif db_instance_status == 'stopped':
                # If the instance is stopped, start it
                print(f"Starting RDS instance {db_instance_id}")
                rds_client.start_db_instance(DBInstanceIdentifier=db_instance_id)
            else:
                print(f"RDS instance {db_instance_id} is in {db_instance_status} state; no action taken.")

        return {
            'statusCode': 200,
            'body': 'Successfully toggled RDS instance states.'
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
