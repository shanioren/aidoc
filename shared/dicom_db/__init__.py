import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'dicom'


# Insert data into the table
def insert_item(patient_id, study_date):
    try:
        table = dynamodb.Table(table_name)
        table.put_item(
            Item={
                'PatientID': patient_id,
                'StudyDate': study_date,
            }
        )
        print(f"Item inserted: {patient_id} ({study_date})")
    except ClientError as e:
        print(f"Error inserting item: {e}")

# Query the table
def query_item(patient_id, study_date):
    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(
            Item={
                'PatientID': patient_id,
                'StudyDate': study_date,
            }
        )
        item = response.get('Item')
        if item:
            print(f"Found item: {item}")
        else:
            print("Item not found")
    except ClientError as e:
        print(f"Error querying item: {e}")


# Delete an item
def delete_item(patient_id, study_date):
    try:
        table = dynamodb.Table(table_name)
        table.delete_item(
            Item={
                'PatientID': patient_id,
                'StudyDate': study_date,
            }
        )
        print(f"Item deleted: {patient_id} ({study_date})")
    except ClientError as e:
        print(f"Error deleting item: {e}")
