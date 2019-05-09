IMAGE_LABEL := krizex/scv
CONTAINER_PORT := 8000
HOST_DEBUG_PORT := 8000
HOST_RUN_PORT := 8080
CUR_DIR := $(shell pwd)
APP_CONTAINER_NAME := scv

.PHONY: build
build:
	mkdir -p _build/datatmp
	docker build -t $(IMAGE_LABEL) .

.PHONY: debug
debug:
	docker run -it --rm \
	--name $(APP_CONTAINER_NAME) \
	-p $(HOST_DEBUG_PORT):$(CONTAINER_PORT) \
	-v $(CUR_DIR)/src:/app \
	-v /etc/localtime:/etc/localtime:ro \
	$(IMAGE_LABEL):latest /bin/bash

.PHONY: run stop restart attach

run:
	docker run --rm -d \
	--name $(APP_CONTAINER_NAME) \
	-p $(HOST_RUN_PORT):$(CONTAINER_PORT) \
	-v /etc/localtime:/etc/localtime:ro \
	$(IMAGE_LABEL):latest

attach:
	docker exec -it $(APP_CONTAINER_NAME) /bin/bash

stop:
	docker stop $(APP_CONTAINER_NAME)

restart: stop run


.PHONY: push pull
push:
	docker push ${IMAGE_LABEL}

pull:
	docker pull ${IMAGE_LABEL}
