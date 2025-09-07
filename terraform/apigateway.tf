resource "aws_api_gateway_rest_api" "resume_api" {
  name        = "resume-rest-api"
  description = "API Gateway for Resume REST Lambda"
  binary_media_types = ["application/pdf"]
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  parent_id   = aws_api_gateway_rest_api.resume_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id             = aws_api_gateway_rest_api.resume_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.proxy.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.resume_api.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.resume_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.resume_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "resume_api" {
  depends_on = [
    aws_api_gateway_integration.lambda,
    aws_api_gateway_integration.swagger_ui_lambda,
    aws_api_gateway_integration.openapi_json_lambda
  ]
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
}

resource "aws_api_gateway_stage" "prod" {
  rest_api_id    = aws_api_gateway_rest_api.resume_api.id
  deployment_id  = aws_api_gateway_deployment.resume_api.id
  stage_name     = "prod"
}

resource "aws_api_gateway_resource" "swagger_ui" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  parent_id   = aws_api_gateway_rest_api.resume_api.root_resource_id
  path_part   = "swagger-ui"
}

resource "aws_api_gateway_resource" "openapi_json" {
  rest_api_id = aws_api_gateway_rest_api.resume_api.id
  parent_id   = aws_api_gateway_rest_api.resume_api.root_resource_id
  path_part   = "openapi.json"
}

resource "aws_api_gateway_method" "swagger_ui_get" {
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  resource_id   = aws_api_gateway_resource.swagger_ui.id
  http_method   = "GET"
  authorization = "NONE"
  api_key_required = false
}

resource "aws_api_gateway_method" "openapi_json_get" {
  rest_api_id   = aws_api_gateway_rest_api.resume_api.id
  resource_id   = aws_api_gateway_resource.openapi_json.id
  http_method   = "GET"
  authorization = "NONE"
  api_key_required = false
}

resource "aws_api_gateway_integration" "swagger_ui_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.resume_api.id
  resource_id             = aws_api_gateway_resource.swagger_ui.id
  http_method             = aws_api_gateway_method.swagger_ui_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.resume_api.invoke_arn
}

resource "aws_api_gateway_integration" "openapi_json_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.resume_api.id
  resource_id             = aws_api_gateway_resource.openapi_json.id
  http_method             = aws_api_gateway_method.openapi_json_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.resume_api.invoke_arn
}