#!make
ifneq (,)
	$(error This Makefile requires GNU Make)
endif

# ─── Variables ────────────────────────────────────────────────────────────────
PROJECT_NAME   ?= diy-stream-deck
PYTHON         ?= python3
PIP            ?= pip

.DEFAULT_GOAL := help

.PHONY: $(shell grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | cut -d":" -f1 | tr "\n" " ")

help: ## Display this help message
	@echo "==================================================================="
	@echo "  $(PROJECT_NAME)"
	@echo "==================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo "==================================================================="

# ─── Installation ─────────────────────────────────────────────────────────────

install: ## Install package dependencies
	$(PIP) install -e "."

dev: ## Install package + dev dependencies
	$(PIP) install -e ".[dev]"

pre-commit: ## Install and run pre-commit hooks
	$(PIP) install --quiet pre-commit
	pre-commit install
	pre-commit run --all-files

# ─── Quality ──────────────────────────────────────────────────────────────────

lint: ## Run ruff linting
	ruff check diy_stream_deck/

format: ## Run ruff formatter
	ruff format diy_stream_deck/

type-check: ## Run mypy type checking
	mypy diy_stream_deck/

# ─── Tests ────────────────────────────────────────────────────────────────────

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ -v --cov=diy_stream_deck --cov-report=term-missing --cov-report=xml

# ─── Cleanup ──────────────────────────────────────────────────────────────────

clean: ## Clean build artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage coverage.xml dist build
