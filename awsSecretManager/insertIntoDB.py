import mysql.connector
import boto3
import json

accessKey = ''
secretKey =  ''

client = boto3.client('secretsmanager',
                        aws_access_key_id=accessKey,
                        aws_secret_access_key=secretKey
                    )

response = client.get_secret_value(
    SecretId='database1Secret1'
)
secretDict = json.loads(response['SecretString'])

mydb = mysql.connector.connect(
    host = secretDict['host'],
    user = secretDict['username'],
    passwd = secretDict['password'],
    database = secretDict['dbname']
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

#mycursor.execute("CREATE DATABASE rahulkDB")
sqlQuery = "INSERT into customers (name, address) VALUES (%s, %s)"
val = ("shahid", "Karnataka")
mycursor.execute(sqlQuery, val)
mydb.commit()
print(mycursor.rowcount,"Record Inserted Successfully")
