import json
import os
import pydicom

import layer.s3 as s3
import layer.dicom_db as dicom_db


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

            # Load the DICOM file
            dicom_file_path = f"/tmp/{file_name}"
            print(dicom_file_path)
            s3.download_file(bucket_name=bucket_name, file_key=file_key, local_file_path=dicom_file_path)

            ds = pydicom.dcmread(dicom_file_path)

            # Extract metadata
            print("Patient Name:", ds.PatientName)
            print("Patient ID:", ds.PatientID)
            print("Modality:", ds.Modality)
            print("Study Date:", ds.StudyDate)

            # Print all metadata
            for element in ds:
                print(element)

            # Write metadata to DynamoDB
            dicom_db.insert_item(patient_id=ds.PatientID, study_date=ds.StudyDate)

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
