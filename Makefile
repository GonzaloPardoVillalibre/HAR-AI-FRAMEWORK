# LINUX Makefile
PROJECT_NAME := framework

define help

Usage: make <command>

Commands:
  help:					Show this help information
  develenv-up:			Launch the 'develenv' environment with a docker-compose of the service
  develenv-up-recreate: Launch the 'develenv' environment with a docker-compose of the service recreating images
  develenv-sh:			Enter into the 'develenv' environment
  develenv-down:		Stop the 'develenv' environment

  Same commands are available for the following environments:
  tunning: 				Adapt any dataset to the required format for this framework
  preprocess:        	Prepare data for a given experiment
  train:				Train and evaluate a neural network
  inference:         	Deploy a model in production 

endef
export help

help:
	@echo "$$help"

develenv-up:	
	@echo "Launching development environments"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d

develenv-up-recreate:	
	@echo "Launching development environments"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate

develenv-down:
	@echo "Shutting down development environments"
	docker-compose -p $(PROJECT_NAME) down --remove-orphans

tunning-up:
	@echo "Launching tunning environment"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate tunning

tunning-sh:
	@echo "Entering tunning environment"
	docker exec -it "tunning" bash

tunning-down:	
	@echo "Shutting down tunning environment"
	docker kill tunning
	docker rm tunning

preprocess-up:	
	@echo "Launching preprocess environment"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate preprocess

preprocess-sh:
	@echo "Entering pre-process environment"
	docker exec -it "preprocess" bash

preprocess-down:	
	@echo "Shutting down preprocess environment"
	docker kill preprocess
	docker rm preprocess

train-up:	
	@echo "Launching preprocess environment"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate train

train-sh:
	@echo "Entering train environment"
	docker exec -it "train" bash

train-down:	
	@echo "Shutting down train environment"
	docker kill train
	docker rm train

inference-up:	
	@echo "Launching inference environment"
	docker-compose build 
	docker-compose -p $(PROJECT_NAME) up -d --build --force-recreate inference

inference-sh:
	@echo "Entering inference environment"
	docker exec -it "inference" bash

inference-down:	
	@echo "Shutting down inference environment"
	docker kill inference
	docker rm inference