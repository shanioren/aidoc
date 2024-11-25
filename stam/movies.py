import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Create a DynamoDB table
def create_table():
    try:
        table = dynamodb.create_table(
            TableName='Movies',
            KeySchema=[
                {
                    'AttributeName': 'Year',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'Title',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Year',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'Title',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table created successfully!")
        return table
    except ClientError as e:
        print(f"Error creating table: {e}")
        return None

# Insert data into the table
def insert_item(year, title, director, genre):
    try:
        table = dynamodb.Table('Movies')
        table.put_item(
            Item={
                'Year': year,
                'Title': title,
                'Director': director,
                'Genre': genre
            }
        )
        print(f"Item inserted: {title} ({year})")
    except ClientError as e:
        print(f"Error inserting item: {e}")

# Query the table
def query_item(year, title):
    try:
        table = dynamodb.Table('Movies')
        response = table.get_item(
            Key={
                'Year': year,
                'Title': title
            }
        )
        item = response.get('Item')
        if item:
            print(f"Found item: {item}")
        else:
            print("Item not found")
    except ClientError as e:
        print(f"Error querying item: {e}")

# Update an item
def update_item(year, title, new_director):
    try:
        table = dynamodb.Table('Movies')
        table.update_item(
            Key={
                'Year': year,
                'Title': title
            },
            UpdateExpression="set Director = :d",
            ExpressionAttributeValues={
                ':d': new_director
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Item updated: {title} ({year})")
    except ClientError as e:
        print(f"Error updating item: {e}")

# Delete an item
def delete_item(year, title):
    try:
        table = dynamodb.Table('Movies')
        table.delete_item(
            Key={
                'Year': year,
                'Title': title
            }
        )
        print(f"Item deleted: {title} ({year})")
    except ClientError as e:
        print(f"Error deleting item: {e}")

if __name__ == '__main__':
    # Create the table if it doesn't exist
    create_table()

    # Insert sample data
    insert_item(2024, 'Movie A', 'Director 1', 'Action')
    insert_item(2023, 'Movie B', 'Director 2', 'Comedy')

    # Query the table
    query_item(2024, 'Movie A')

    # Update an item
    update_item(2024, 'Movie A', 'Director 3')

    # Delete an item
    delete_item(2023, 'Movie B')
