NAME := starbucksdb
ENVIRONMENT ?= development

SHELL=/bin/bash
POETRY := $(shell command -v poetry 2> /dev/null)
DATASETTE := $(shell command -v datasette 2> /dev/null)
SQLITE_FILE = data/starbucks.db


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
	@rm -rf data/starbucks.db
	@$(POETRY) run scrapy crawl singapore
	@echo "Done."
datasette:	## run datasette.
	@[ -f $(SQLITE_FILE) ] && echo "File $(SQLITE_FILE) exists." || { echo "File $(SQLITE_FILE) does not exist." >&2; exit 1; }
	@$(DATASETTE) $(SQLITE_FILE) --metadata data/metadata.json


##@ Contributing
.PHONY: clean
clean:	## clean all local cache.
	@find . -type d -name "__pycache__" | xargs rm -rf {};
	@rm -rf .scrapy
