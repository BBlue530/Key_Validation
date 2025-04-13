import json
from datetime import datetime, timedelta
import boto3
import uuid

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1", endpoint_url="https://dynamodb.eu-north-1.amazonaws.com")
table = dynamodb.Table("Key_Validation")
secrets_client = boto3.client("secretsmanager")

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
    expiration_days = 30

    try:
        body = json.loads(event["body"])
        client_name = body["name"]

    except KeyError as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }
    except json.JSONDecodeError as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON input"})
        }

    license_key = str(uuid.uuid4())

    # Expiration date
    expiration_date = (datetime.now() + timedelta(days=expiration_days)).strftime("%Y-%m-%d")

    # Store key in DynamoDB
    table.put_item(
        Item={
            "LicenseKey": license_key,
            "ClientName": client_name,
            "ExpirationDate": expiration_date,
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"License Key Generated: {client_name}: {license_key} Expire: {expiration_date}"})
    }

##################################################################################################################################

def get_secret():
    secret_name = "Key_Validation_API_Key"
    region_name = "eu-north-1"

    try:
        get_secret_value_response = secrets_client.get_secret_value(SecretId=secret_name)
        print(f"Secret retrieved: {get_secret_value_response}") # Debug
        
        # Check if secret is a string
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            # Binary secrets
            decoded_binary_secret = get_secret_value_response["SecretBinary"]
            secret = decoded_binary_secret.decode("utf-8")
        
        return json.loads(secret)["api_key"]

    except Exception as e:
        print(f"Error retrieving secret: {str(e)}")
        raise Exception("Error retrieving API key from Secrets Manager")
    
##################################################################################################################################

def lambda_handler(event, context):
    print(json.dumps(event))
    try:
        secret_api_key = get_secret()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal error: Unable to retrieve API key"})
        }
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

        if api_key == secret_api_key:
            response = create_key(event)
            return response
        else:
            print("Invalid Key")
            return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }

##################################################################################################################################