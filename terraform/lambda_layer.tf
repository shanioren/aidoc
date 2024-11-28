resource "aws_s3_object" "dummy_lambda_layer_code" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key    = "layer/layer.zip"
  acl    = "private"
  source = data.archive_file.lambda_dummy_zip.output_path
}


# Create Lambda Layer
resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name  = "dicom-lambda-layer"
  description = "A Lambda layer for shared dependencies"

  s3_bucket = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key    = "layer/layer.zip"  # This is the path in your S3 bucket

  compatible_runtimes = [var.lambda.runtime]
}
