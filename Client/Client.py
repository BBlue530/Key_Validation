import requests
import json

# PLEASE WORK I BEG OF YOU
def validate_license(license_key):
    url = "https://u1e8fkkqcl.execute-api.eu-north-1.amazonaws.com/v1/CheckKey"
    headers = {
        "Content-Type": "application/json"
    }

    # The body should be wrapped like API Gateway does it: {"body": "<json-string>"}
    event_payload = {
        "body": json.dumps({
            "LicenseKey": license_key
        }),
        "rawPath": "/v1/CheckKey"
    }

    # Send as JSON
    response = requests.post(url, headers=headers, data=json.dumps(event_payload))

    if response.status_code == 200:
        print("License = valid")
    else:
        try:
            error_message = response.json().get("message", "Unknown error")
        except json.JSONDecodeError:
            error_message = "Non-JSON error response"
        print(f"License validation failed: {error_message}")

if __name__ == "__main__":
    license_key = input("Enter license key: ")
    validate_license(license_key)
