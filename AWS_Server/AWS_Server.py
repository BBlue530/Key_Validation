import json
from datetime import datetime
import boto3

# I WILL APPEAR IF EVERYTHING WORKED LIKE IT SHOULD

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1", endpoint_url="https://dynamodb.eu-north-1.amazonaws.com")
table = dynamodb.Table("Key_Validation")

def check_key(event):
    try:
        body = json.loads(event["body"])
        license_key = body["LicenseKey"]
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }
    try:
        response = table.get_item(Key={"LicenseKey": license_key})
        if "Item" not in response:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "LicenseKey: not found"})
            }

        license = response["Item"]
        expiration_date = license["ExpirationDate"]
        if datetime.strptime(expiration_date, "%Y-%m-%d") < datetime.now():
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "LicenseKey: expired"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "LicenseKey: valid"})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal error", "error": str(e)})
        }

def lambda_handler(event, context):
    print(json.dumps(event))
    try:
        endpoint = event["rawPath"]
    except KeyError as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }
    
    if endpoint == "/v1/CheckKey":
        response = check_key(event)
        return response