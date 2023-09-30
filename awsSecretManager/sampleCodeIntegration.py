# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import mysql.connector
import boto3
from botocore.exceptions import ClientError
import boto3.session
import json


def get_secret():

    secret_name = "azVMSecret"
    region_name = "ap-south-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = json.loads(get_secret_value_response['SecretString'])

    print(secret)
    print(type(secret))

    # Your code goes here.
    mydb = mysql.connector.connect(
        host = secret['host'],
        user = secret['username'],
        passwd = secret['password'],
        database = secret['dbname']
    )

    mycursor = mydb.cursor()
    #mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

    #mycursor.execute("CREATE DATABASE rahulkDB")
    sqlQuery = "INSERT into customers (name, address) VALUES (%s, %s)"
    val = ("rahulksharma1", "West Bengal")
    mycursor.execute(sqlQuery, val)
    mydb.commit()
    print(mycursor.rowcount,"Record Inserted Successfully")
get_secret()

