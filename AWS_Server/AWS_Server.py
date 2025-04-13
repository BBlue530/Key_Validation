import json
from datetime import datetime, timedelta
import boto3
import uuid

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1", endpoint_url="https://dynamodb.eu-north-1.amazonaws.com")
table = dynamodb.Table("Key_Validation")

##################################################################################################################################

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
    
##################################################################################################################################
    
def create_key(event):
    dynamodb = boto3.resource("dynamodb", region_name="eu-north-1", endpoint_url="https://dynamodb.eu-north-1.amazonaws.com")
    table = dynamodb.Table("Key_Validation")
    expiration_days=30

    try:
        body = json.loads(event["body"])
        client_name = body["name"]
    except KeyError as e:
        print(f"Error: {str(e)}")
        return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid input"})
          }

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

    return {
                "statusCode": 200,
                "body": json.dumps({"message": f"License Key Generated: {client_name}: {license_key} Expire: {expiration_date})"})
          }

##################################################################################################################################

def lambda_handler(event):
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
    elif endpoint == "/v1/CreateKey":
        try:
            api_key = event["headers"]["key"]
        except KeyError as e:
            print(f"Error: {str(e)}")
            return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }

        if api_key == "12345":
            response = create_key(event)
            return response
        else:
            print("Invalid Key")
            return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }

##################################################################################################################################