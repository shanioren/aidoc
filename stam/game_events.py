from datetime import datetime
from xmlrpc.client import DateTime

import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table_name = 'GameEvents'

def insert_item(player_id: str, date: str, game_round_id: str, score: str):
    try:
        table = dynamodb.Table(table_name)
        table.put_item(
            Item={
                'playerId': player_id,
                'Date': date,
                'gameRoundId': game_round_id,
                'score': score
            }
        )
        print(f"Item inserted: {player_id} ({date})")
    except ClientError as e:
        print(f"Error inserting item: {e}")


# Update an item
def update_item(player_id: str, date: str, updated_score: str):
    try:
        table = dynamodb.Table(table_name)
        table.update_item(
            Key={
                'playerId': player_id,
                'Date': date,
            },
            UpdateExpression="set score = :d",
            ExpressionAttributeValues={
                ':d': updated_score
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"Item updated: {player_id} ({date})")
    except ClientError as e:
        print(f"Error updating item: {e}")

# Delete an item
def delete_item(player_id: str, date: str):
    try:
        table = dynamodb.Table(table_name)
        table.delete_item(
            Key={
                'playerId': player_id,
                'Date': date,
            }
        )
        print(f"Item deleted: {player_id} ({date})")
    except ClientError as e:
        print(f"Error deleting item: {e}")

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # Insert sample data
    insert_item('1', dt_string, 'round 1', '100')
    insert_item('2', dt_string, 'round 1', '10')

    # Update an item
    update_item('1', dt_string, '130')

    # Delete an item
    delete_item('2', dt_string)
