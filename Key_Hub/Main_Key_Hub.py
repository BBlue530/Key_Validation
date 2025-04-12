import boto3
import uuid
from datetime import datetime, timedelta

# Initialize the DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="eu-north-1", endpoint_url="https://dynamodb.eu-north-1.amazonaws.com")
table = dynamodb.Table("Key_Validation")

def generate_license_key(client_name, expiration_days=30):
    license_key = str(uuid.uuid4())

    # Expiration date
    expiration_date = (datetime.now() + timedelta(days=expiration_days)).strftime("%Y-%m-%d")

    # Store key DynamoDB
    table.put_item(
    Item={
        "LicenseKey": license_key,
        "ClientName": client_name,
        "ExpirationDate": expiration_date,
    }
)

    print(f"License Key Generated: {client_name}: {license_key} Expire: {expiration_date})")
    print(f"License Key: {license_key}")

if __name__ == "__main__":
    client_name = input("Enter client name: ")
    generate_license_key(client_name)