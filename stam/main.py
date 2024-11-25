import os

import s3
import pydicom


if __name__ == '__main__':
    for file_key in s3.iterate_files(bucket_name='aidoc1', prefix='Circle of Willis/'):
        print(file_key)

        # Extract file name and extension
        file_name = os.path.basename(file_key)  # example.txt
        file_extension = os.path.splitext(file_name)[1]  # .txt

        if file_extension != '.dcm':
            continue

        s3.download_file(bucket_name='aidoc1', file_key=file_key, local_file_path=file_name)

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