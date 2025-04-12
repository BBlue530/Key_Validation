import requests
import json

# PLEASE WORK I BEG OF YOU
def validate_license(license_key):
    url = "https://xqj059pfvi.execute-api.eu-north-1.amazonaws.com/V1"
    headers = {"Content-Type": "application/json"}

    data = {
        "LicenseKey": license_key
    }

    # Request the API
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("License = valid")
    else:
        print(f"License validation failed: {response.json().get("message", "Unknown error")}")

if __name__ == "__main__":
    license_key = input("Enter license key: ")
    validate_license(license_key)