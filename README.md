License Key Validation System:
This project allows me to generate, store, and validate license keys. I use AWS services like DynamoDB, Lambda, and CodeBuild to manage and deploy the system. Clients can check if their license key is valid or expired by running it through the Lambda function.

Features:
Generate License Keys: I can create a new license key with an expiration date.

Store License Keys: The license keys and their details are stored in DynamoDB.

Validate License Keys: Clients can check if their license key is valid by invoking a Lambda function.

Automatic Updates: Code updates to the Lambda function are deployed automatically using AWS CodeBuild.

Components:
1. Main_Key_Hub.py - License Key Generator
This script lets me generate a new license key and store it in DynamoDB.

I enter a client name, and the script generates a unique license key tied to that client.

It also sets an expiration date (default is 30 days) and stores this information in the DynamoDB table Key_Validation.

2. AWS_Server.py - Lambda Function to Validate License
This is the Lambda function that validates the license key. When a client sends their license key, this function checks if the key exists in DynamoDB and if it’s expired.

Here’s how it works:

It receives the license key from the client.

It checks DynamoDB for the license key and verifies if it has expired.

It returns whether the key is valid, expired, or not found.

3. Client.py - Client-Side Validation
This script lets the client validate their license key. The client sends a POST request to the Lambda function with the license key, and the Lambda function returns whether the key is valid or expired.

To use it:

The client enters their license key.

The script sends the key to the Lambda function for validation.

Deployment:
I use AWS CodeBuild to deploy updates to the Lambda function automatically. Here’s how it works:

Buildspec: When I push new code, CodeBuild packages the Lambda function and updates the Lambda code.

DynamoDB: The license key data is stored in the Key_Validation table.

Technologies Used
AWS Lambda: To run the serverless function for validating license keys.

DynamoDB: To store the license keys and related information.

AWS CodeBuild: For automating the deployment of Lambda code.

How to Use:
Generate a license key using Main_Key_Hub.py.

Deploy the Lambda function using the AWS Lambda console.

Clients can use Client.py to validate their license keys.

Code updates are automatically deployed using AWS CodeBuild.
