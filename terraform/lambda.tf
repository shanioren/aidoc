data "aws_s3_bucket" "dicom" {
  bucket = "aidoc1"
}

data "aws_dynamodb_table" "dicom" {
  name = "dicom"
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "shani_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "shani_lambda_policy" {
  name = "shani_lambda_policy"
  role = aws_iam_role.lambda_execution_role.id
  policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "dynamodb:PutItem",
            "dynamodb:GetItem",
            "dynamodb:UpdateItem"
          ]
          Resource = "${data.aws_dynamodb_table.dicom.arn}"
        },
        {
          Effect = "Allow"
          Action = [
            "s3:GetObject"
          ]
          Resource = "${data.aws_s3_bucket.dicom.arn}/dicom/*"
        },
        {
          Effect = "Allow"
          Action = [
            "s3:ListBucket"
          ]
          Resource = "${data.aws_s3_bucket.dicom.arn}/dicom/"
        },
        {
            Effect   = "Allow"
            Action   = "s3:GetObject"
            Resource = [
              "${aws_s3_bucket.lambda_code_bucket.arn}/*"
            ]
        }
      ]
    })
}

# Attach policies to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_basic_policy" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_s3_object" "dummy_lambda_code" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key    = "lambda/lambda.zip"
  source = data.archive_file.lambda_dummy_zip.output_path
  acl    = "private"
#   content_type = "application/zip"
}


# Lambda Function
resource "aws_lambda_function" "lambda" {
  function_name = "s3_to_dynamodb"
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = var.lambda.handler
  runtime       = var.lambda.runtime

  s3_bucket     = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key        = "lambda/lambda.zip"  # This is the path in your S3 bucket

  # Attach the Layer
  layers = [aws_lambda_layer_version.lambda_layer.arn]
}

# Grant S3 permission to invoke Lambda
resource "aws_lambda_permission" "allow_s3_trigger" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.arn
  principal     = "s3.amazonaws.com"
  source_arn    = data.aws_s3_bucket.dicom.arn
}

# Configure S3 to trigger Lambda on object creation
resource "aws_s3_bucket_notification" "s3_trigger" {
  bucket = data.aws_s3_bucket.dicom.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda.arn
    filter_prefix       = "dicom/"
    events              = ["s3:ObjectCreated:*"] # Trigger on all object creation events
  }

  depends_on = [aws_lambda_permission.allow_s3_trigger]
}

# resource "aws_s3_bucket" "bucket_read_videos" {
#   bucket        = var.bucket_for_videos
# }
#
# resource "aws_s3_bucket_notification" "bucket_notification" {
#   bucket = aws_s3_bucket.bucket_read_videos.id
#
#   lambda_function {
#     lambda_function_arn = aws_lambda_function.aws_lambda_test.arn
#     events = ["s3:ObjectCreated:*"]
#     filter_suffix = ".mp4"
#   }
# }


