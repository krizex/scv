IMAGE_LABEL := krizex/scv
CONTAINER_PORT := 8000
HOST_DEBUG_PORT := 8000
CUR_DIR := $(shell pwd)
APP_CONTAINER_NAME := scv
DB_CONTAINER_NAME := scv-pg

.PHONY: build
build:
	mkdir -p _build/datatmp
	docker build -t $(IMAGE_LABEL) .

.PHONY: debug
debug:
	docker run -it --rm \
	--name $(APP_CONTAINER_NAME) \
	--link $(DB_CONTAINER_NAME) \
	--env-file database.conf \
	-p $(HOST_DEBUG_PORT):$(CONTAINER_PORT) \
	-v $(CUR_DIR)/src:/app \
	-v /etc/localtime:/etc/localtime:ro \
	-v /var/scv/running:/app/scv/running:rw \
	$(IMAGE_LABEL):latest /bin/bash

.PHONY: run-pg stop-pg
run-pg:
	docker run --rm -d \
	--name $(DB_CONTAINER_NAME) \
	--env-file database.conf \
	-v /var/scv-pg/db:/var/lib/postgresql/data:rw \
	postgres:10-alpine

stop-pg:
	docker stop $(DB_CONTAINER_NAME)

#####################################

.PHONY: run stop restart attach

run:
	docker-compose up -d

attach:
	docker exec -it $(APP_CONTAINER_NAME) /bin/bash

stop:
	docker-compose down

restart: stop run


#####################################
.PHONY: push pull
push:
	docker push ${IMAGE_LABEL}

pull:
	docker pull ${IMAGE_LABEL}
