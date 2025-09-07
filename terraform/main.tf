terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "aws" {
  region = var.aws_region
}


resource "aws_dynamodb_table" "companies" {
  name           = "companies"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "institutions" {
  name           = "institutions"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "contact_info" {
  name           = "contact_info"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "blocklist" {
  name           = "blocklist"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "users" {
  name           = "users"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "skills" {
  name           = "skills"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "resume_questions" {
  name           = "resume_questions"
  hash_key       = "id"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_lambda_function" "resume_api" {
  function_name = var.lambda_function_name
  handler       = "src.app.lambda_handler"
  runtime       = "python3.12"
  filename      = "../lambda_package.zip"
  source_code_hash = filebase64sha256("../lambda_package.zip")

  environment {
    variables = {
      COMPANIES_TABLE    = aws_dynamodb_table.companies.name
      INSTITUTIONS_TABLE = aws_dynamodb_table.institutions.name
      SKILLS_TABLE       = aws_dynamodb_table.skills.name
      CONTACT_INFO_TABLE = aws_dynamodb_table.contact_info.name
      BLOCKLIST_TABLE    = aws_dynamodb_table.blocklist.name
      USERS_TABLE        = aws_dynamodb_table.users.name
      JWT_SECRET_KEY     = var.jwt_secret_key
      GEMINI_API_KEY     = var.gemini_api_key
      PYTHONPATH = "/var/task/src"
    }
  }

  role = aws_iam_role.lambda_exec.arn
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.lambda_exec.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:*",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}


