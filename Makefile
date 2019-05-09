.PHONY: build tag push

build:
	docker build -t helloworld .

tag:
	docker tag helloworld:latest sahaanirban/helloworld:latest

push:
	docker push sahaanirban/helloworld:latest

release: build tag push
