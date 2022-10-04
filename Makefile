# LINUX Makefile
PROJECT_NAME := framework

define help

Usage: make <command>

Commands:
  help:                 Show this help information
  develenv-up:          Launch the development environment with a docker-compose of the service
  develenv-up-recreate: Launch the development environment with a docker-compose of the service recreating images
  preprocess-up:        Launch only the preprocess environment from the docker-compose recreating images
  train-up:             Launch only the train environment from the docker-compose recreating images
  inference-up:         Launch only the inference environment from the docker-compose recreating images
  preprocess-sh:        Access to a shell of a launched pre-process environment
  train-sh:             Access to a shell of a launched training environment
  inference-sh:         Access to a shell of a launched inference environment
  preprocess-down:      Stop the only the preprocess environment
  train-down:           Stop the only the train environment
  inference-down:       Stop the only the inferencema environment
  develenv-down:        Stop the development environment

endef
export help

help:
	@echo "$$help"

develenv-up:	
	@echo "Launching development environments"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d

preprocess-up:	
	@echo "Launching preprocess environment"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate preprocess

preprocess-down:	
	@echo "Shutting down preprocess environment"
	docker kill preprocess
	docker rm preprocess

train-up:	
	@echo "Launching train environment"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate train

train-down:	
	@echo "Shutting down train environment"
	docker kill train
	docker rm train

inference-up:
	@echo "Launching inference environment"
	docker-compose build
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate inference

inference-down:
	@echo "Shutting down inference environment"
	docker kill inference
	docker rm inference

develenv-up-recreate:	
	@echo "Launching development environments"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate

develenv-down:
	@echo "Shutting down development environments"
	docker-compose -p $(PROJECT_NAME) down --remove-orphans

preprocess-sh:
	@echo "Entering pre-process environment"
	docker exec  -it "preprocess" bash

train-sh:
	@echo "Entering train environment"
	docker exec -it "train" bash

inference-sh:
	@echo "Entering inference environment"
	docker exec -it "inference" bash
