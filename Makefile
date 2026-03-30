deps:
	uv sync

lint:
	uv run ruff format
	uv run ruff check --fix

start:
	uv run avni-ai-server

test:
	uv run pytest --cov=.

test-integration:
	python -m tests.dify.config.mch_integration_test

build-and-deploy-to-staging:
	tar -czf /tmp/avni-ai.tar.gz \
		--exclude='.git' \
		--exclude='.venv' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.pytest_cache' \
		.
	scp /tmp/avni-ai.tar.gz avni-staging:/tmp/avni-ai.tar.gz
	ssh avni-staging "sudo tar -xzf /tmp/avni-ai.tar.gz -C /opt/avni-ai/current && sudo chown -R avni-ai-user:avni-ai-grp /opt/avni-ai/current && sudo systemctl reset-failed avni-ai; sudo systemctl restart avni-ai"
