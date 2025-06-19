default:
	SHELLPOKER_LOGLEVEL=DEBUG uv run shellpoker

test:
	uv run pytest
 
lint:
	uv run ruff check --fix
