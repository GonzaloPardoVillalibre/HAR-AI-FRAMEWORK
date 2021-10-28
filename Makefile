# LINUX Makefile
PROJECT_NAME := framework

define help

Usage: make <command>

Commands:
  help:                 Show this help information
  develenv-up:          Launch the development environment with a docker-compose of the service
  develenv-up-recreate: Launch the development environment with a docker-compose of the service recreating images
  preprocess-sh:        Access to a shell of a launched preprocessing environment
  train-sh:             Access to a shell of a launched training environment
  inference-sh:         Access to a shell of a launched inference environment
  develenv-down:        Stop the development environment

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

preprocess-sh:
	@echo "Entering preprocessing environment"
	docker exec -it "preprocesser" bash

train-sh:
	@echo "Entering train environment"
	docker exec -it "trainer" bash

inference-sh:
	@echo "Entering inference environment"
	docker exec -it "inferencer" bash
