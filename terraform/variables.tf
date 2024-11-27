
variable "lambda" {
    type = object({
        runtime         = string
        layer_zip_file  = string
        zip_file        = string
        handler         = string
    })
    default = {
        runtime         = "python3.12"
        layer_zip_file  = "layer.zip"
        zip_file        = "lambda.zip"
        handler         = "lambda.dicom_file_processor.lambda_handler"
    }
}

#
# variable "lambda" {
#     type = map(object({
#         runtime = "python3.12"
#         layer_zip_file = "layer.zip"
#         zip_file = "lambda.zip"
#     }))
# }