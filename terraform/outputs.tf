output "lambda_function_name" {
  value = aws_lambda_function.resume_api.function_name
}

output "api_gateway_url" {
  value       = aws_api_gateway_stage.prod.invoke_url
  description = "Base URL for the deployed API Gateway"
}

output "lambda_function_arn" {
  value       = aws_lambda_function.resume_api.arn
  description = "ARN of the deployed Lambda function"
}

output "dynamodb_table_names" {
  value = [
    aws_dynamodb_table.companies.name,
    aws_dynamodb_table.institutions.name,
    aws_dynamodb_table.skills.name,
    aws_dynamodb_table.contact_info.name,
    aws_dynamodb_table.blocklist.name,
    aws_dynamodb_table.users.name,
    aws_dynamodb_table.resume_questions.name
  ]
  description = "Names of all DynamoDB tables used by the API"
}
