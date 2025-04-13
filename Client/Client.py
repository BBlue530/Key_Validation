import requests
import json

def create_license():
    client_name = input("Enter client name: ")
    api_key = input("Enter API key: ")

    url = "https://u1e8fkkqcl.execute-api.eu-north-1.amazonaws.com/v1/CreateKey"
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

def validate_license(license_key):
    url = "https://u1e8fkkqcl.execute-api.eu-north-1.amazonaws.com/v1/CheckKey"
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

if __name__ == "__main__":
    while True:
        print("1. Check license")
        print("2. Create new license")
        print("3. Exit")

        choice = input("CLI: ")

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