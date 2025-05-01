from fastapi import FastAPI, Header, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import boto3
import uuid
import json
import os

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1", endpoint_url="https://dynamodb.eu-north-1.amazonaws.com")
table = dynamodb.Table("Key_Validation")
secrets_client = boto3.client("secretsmanager", region_name="eu-north-1")

app = FastAPI()

class LicenseRequest(BaseModel):
    LicenseKey: str

class CreateRequest(BaseModel):
    name: str

##################################################################################################################################

@app.post("/v1/CheckKey")
def check_key(request: LicenseRequest):
    try:
        response = table.get_item(Key={"LicenseKey": request.LicenseKey})
        if "Item" not in response:
            raise HTTPException(status_code=400, detail="LicenseKey: not found")

        license = response["Item"]
        expiration_date = license["ExpirationDate"]
        if datetime.strptime(expiration_date, "%Y-%m-%d") < datetime.now():
            raise HTTPException(status_code=400, detail="LicenseKey: expired")

        return {"message": "LicenseKey: valid"}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal error")
    
##################################################################################################################################

@app.post("/v1/CreateKey")
def create_key(request: CreateRequest, key: str = Header(...)):
    secret_api_key = get_secret()
    if key != secret_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    license_key = str(uuid.uuid4())
    expiration_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

    table.put_item(
        Item={
            "LicenseKey": license_key,
            "ClientName": request.name,
            "ExpirationDate": expiration_date,
        }
    )

    return {
        "message": f"License Key Generated: {request.name}: {license_key} Expire: {expiration_date}"
    }

##################################################################################################################################

def get_secret():
    secret_name = "Key_Validation_API_Key"
    try:
        get_secret_value_response = secrets_client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = get_secret_value_response["SecretBinary"].decode("utf-8")
        return json.loads(secret)["secret_api_key"]
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise HTTPException(status_code=500, detail="Unable to retrieve API key")
    
##################################################################################################################################