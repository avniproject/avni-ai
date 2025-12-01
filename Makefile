deps:
	uv sync

lint:
	uv run ruff format
	uv run ruff check --fix

start:
	uv run avni-mcp-server

test:
	uv run pytest --cov=.

test-integration:
	python -m tests.dify.config.mch_integration_test
