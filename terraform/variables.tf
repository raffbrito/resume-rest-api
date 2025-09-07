variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "resume-rest-api-lambda"
}


variable "dynamodb_hash_key" {
  description = "Hash key for DynamoDB table"
  type        = string
  default     = "id"
}

variable "gemini_api_key" {
  description = "Google Gemini API key"
  type        = string
  sensitive   = true
}

variable "jwt_secret_key" {
  description = "JWT secret key"
  type        = string
  sensitive   = true
}
