# Variables
AWS_REGION = us-east-1
S3_BUCKET = shani-lambda-code-bucket

LAYER_NAME = dicom-lambda-layer
LAYER_ZIP = layer.zip
LAYER_S3_KEY = layer/$(LAYER_ZIP)

LAMBDA_FUNCTION_NAME = s3_to_dynamodb
LAMBDA_CODE_ZIP = lambda.zip
CODE_S3_KEY = lambda/$(LAMBDA_CODE_ZIP)

LAYER_ARN = $(shell aws lambda list-layer-versions --layer-name $(LAYER_NAME) --region $(AWS_REGION) --query 'LayerVersions[0].LayerVersionArn' --output text)

export AWS_PAGER=""

# Targets

# Default target (run when 'make' is invoked without arguments)
.PHONY: deploy
deploy: upload-layer publish-layer upload-function update-lambda clean

# Upload Lambda Layer to S3
upload-layer:
	@echo "Packaging and uploading Lambda layer..."
	mkdir -p python
	pip install -r requirements.txt -t python/
	cp -r layer python
	zip -r $(LAYER_ZIP) python
	aws s3 cp $(LAYER_ZIP) s3://$(S3_BUCKET)/$(LAYER_S3_KEY) --region $(AWS_REGION)

# Publish Lambda Layer to AWS
publish-layer:
	@echo "Publishing Lambda layer version..."
	aws lambda publish-layer-version \
		--layer-name $(LAYER_NAME) \
		--content S3Bucket=$(S3_BUCKET),S3Key=$(LAYER_S3_KEY) \
		--region $(AWS_REGION)

# Upload Lambda Function Code to S3
upload-function:
	@echo "Packaging and uploading Lambda function..."
	zip -r $(LAMBDA_CODE_ZIP) lambda
	aws s3 cp $(LAMBDA_CODE_ZIP) s3://$(S3_BUCKET)/$(CODE_S3_KEY) --region $(AWS_REGION)

# Deploy Lambda Function (including layer)
update-lambda:
	@echo "Updating Lambda function..."
	aws lambda update-function-code \
		--function-name $(LAMBDA_FUNCTION_NAME) \
		--s3-bucket $(S3_BUCKET) \
		--s3-key $(CODE_S3_KEY) \
		--region $(AWS_REGION)

	@echo "Updating Lambda function to use new layer..."
	aws lambda update-function-configuration \
		--function-name $(LAMBDA_FUNCTION_NAME) \
		--layers $(LAYER_ARN) \
		--region $(AWS_REGION)

# Clean up the generated files
clean:
	@echo "Cleaning up generated files..."
	rm -rf python $(LAYER_ZIP) $(LAMBDA_CODE_ZIP)
