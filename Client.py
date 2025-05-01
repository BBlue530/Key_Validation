import requests
import json

##################################################################################################################################

def create_license():
    client_name = input("Enter client name: ")
    api_key = input("Enter API key: ")

    url = "http://k8s-default-keyvalid-dd3b8a0115-619972b2556ec875.elb.eu-north-1.amazonaws.com/v1/CreateKey"  # LoadBalancer URL
    headers = {
        "Content-Type": "application/json",
        "key": api_key
    }

    data = {
        "name": client_name
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print(f"{response.json()['message']}")
        else:
            print(f"Key creation failed: {response.json().get('message', 'Unknown error')}")

    except Exception as e:
        print(f"Error: {e}")

##################################################################################################################################

def validate_license(license_key):
    url = "http://k8s-default-keyvalid-dd3b8a0115-619972b2556ec875.elb.eu-north-1.amazonaws.com/v1/CheckKey"  # LoadBalancer URL
    headers = {"Content-Type": "application/json"}

    data = {
        "LicenseKey": license_key
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("License = valid")
        else:
            print(f"License validation failed: {response.json().get('message', 'Unknown error')}")

    except Exception as e:
        print(f"Error: {e}")

##################################################################################################################################

if __name__ == "__main__":
    while True:
        print("1. Check license")
        print("2. Create new license")

        choice = input("ඞ: ")

        if choice == "1":
            license_key = input("Enter license key: ")
            validate_license(license_key)
        elif choice == "2":
            create_license()
        elif choice == "3":
            print("Exit...")
            break
        else:
            print("Invalid choice.")