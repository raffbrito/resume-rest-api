# Terraform AWS Lambda + DynamoDB Setup

## Steps

1. Edit `variables.tf` as needed (table name, region, etc).
2. Package your Python app for Lambda (see below).
3. Run:
   ```sh
   terraform init
   terraform apply
   ```

## Packaging Python for Lambda

1. Install dependencies:
   ```sh
   pip install -r requirements.txt -t lambda_build/
   cp app.py lambda_build/
   cd lambda_build
   zip -r ../lambda_package.zip .
   cd ..
   rm -rf lambda_build
   ```
2. Ensure your handler in `app.py` is named `lambda_handler`.
3. The zipped file (`lambda_package.zip`) will be used by Terraform.

## Notes
- The Lambda function will have access to the DynamoDB table via environment variable `DYNAMODB_TABLE`.
- You can extend this setup to add API Gateway if needed.
