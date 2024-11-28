resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket = "shani-lambda-code-bucket"
}

# Create ZIP for the Lambda Layer
data "archive_file" "lambda_dummy_zip" {
  type        = "zip"
  source_file  = "dummy.py"
  output_path = "dummy.py.zip"
}