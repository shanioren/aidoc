# # Create ZIP for the Lambda Layer
# data "archive_file" "layer_zip" {
#   type        = "zip"
#   source_dir  = "../layer"
#   output_path = "../layer.zip"
# }

# Create Lambda Layer
resource "aws_lambda_layer_version" "shared_layer" {
  layer_name  = "dicom-shared-layer"
  filename    = var.lambda.layer_zip_file
  compatible_runtimes = [var.lambda.runtime]
}
