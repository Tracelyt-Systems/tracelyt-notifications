.DEFAULT_GOAL := help

MVN := ./mvnw
ifeq ($(OS),Windows_NT)
	MVN := mvnw.cmd
endif

.PHONY: help
help: ## Display available make targets
	@echo "Tracelyt Notifications - Developer Targets"
	@echo "=========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: validate
validate: ## Run Checkstyle formatting and style audits
	$(MVN) -B -ntp checkstyle:check

.PHONY: test
test: ## Run unit and smoke tests
	$(MVN) -B -ntp test

.PHONY: build
build: ## Package application artifact JAR
	$(MVN) -B -ntp package -DskipTests

.PHONY: docs-check
docs-check: ## Verify Markdown link integrity and scan for accidental credentials
	python tools/validate_docs.py

.PHONY: clean
clean: ## Clean build target directory
	$(MVN) -B -ntp clean
