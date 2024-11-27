.PHONY: build clean

build:
	mkdir -p python
	pip install -r requirements.txt -t python/
	cp -r layer python
	zip -r terraform/layer.zip python
	zip -r terraform/lambda.zip lambda

	cd terraform; terraform apply

clean:
	rm -rf python terraform/layer.zip terraform/lambda.zip
