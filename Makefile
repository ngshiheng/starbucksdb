NAME := starbucksdb
ENVIRONMENT ?= development

SHELL=/bin/bash
POETRY := $(shell command -v poetry 2> /dev/null)
DOCKER := $(shell command -v docker 2> /dev/null)

.DEFAULT_GOAL := help
##@ Helper
.PHONY: help
help:	## display this help message.
	@echo "Welcome to $(NAME) [$(ENVIRONMENT)]."
	@awk 'BEGIN {FS = ":.*##"; printf "Use make \033[36m<target>\033[0m where \033[36m<target>\033[0m is one of:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


##@ Development
.PHONY: dev
dev:	## install packages and prepare environment with poetry.
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	@$(POETRY) install
	@$(POETRY) shell
	@echo "Done."


##@ Usage
.PHONY: run
run:	## run spider.
	@rm -rf assets/starbucks.db
	@$(POETRY) run scrapy crawl singapore
	@echo "Done."


##@ Contributing
.PHONY: clean
clean:	## clean all local cache.
	@find . -type d -name "__pycache__" | xargs rm -rf {};
	@rm -rf .scrapy
