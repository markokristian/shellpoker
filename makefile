default:
	SHELLPOKER_LOGLEVEL=DEBUG SHELLPOKER_LOG_TO_FILE="true" uv run shellpoker

test:
	uv run pytest
 
lint:
	uv run ruff check --fix

simulate:
	uv run python src/shellpoker/simulate.py
