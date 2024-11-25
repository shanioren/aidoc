import json
import os

import boto3
import pydicom


# Initialize clients for S3 and DynamoDB
s3_resource = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Define the DynamoDB table name
DYNAMODB_TABLE_NAME = "dicom"


def lambda_handler(event, context):
    try:
        # Get S3 event details
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            file_key = record['s3']['object']['key']

            # Extract file name and extension
            file_name = os.path.basename(file_key)  # example.txt
            file_extension = os.path.splitext(file_name)[1]  # .txt

            if file_extension != '.dcm':
                continue

            s3_resource.Bucket(bucket_name).download_file(Key=file_key, Filename=file_name)

            # Load the DICOM file
            # dicom_file_path = "example.dcm"  # Replace with your file path
            dicom_file_path = file_name
            ds = pydicom.dcmread(dicom_file_path)

            # Extract metadata
            print("Patient Name:", ds.PatientName)
            print("Patient ID:", ds.PatientID)
            print("Modality:", ds.Modality)
            print("Study Date:", ds.StudyDate)

            # Print all metadata
            for element in ds:
                print(element)

            # # Write metadata to DynamoDB
            # table = dynamodb.Table(DYNAMODB_TABLE_NAME)

        return {
            "statusCode": 200,
            "body": json.dumps("File metadata written successfully!")
        }

    except Exception as e:
        print(f"Error processing event: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }
