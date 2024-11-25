.PHONY: build clean

build:
	mkdir -p python
	pip install -r requirements.txt -t python/
	cp -r shared python
	zip -r shared_layer.zip python

clean:
	rm -rf python shared_layer.zip
