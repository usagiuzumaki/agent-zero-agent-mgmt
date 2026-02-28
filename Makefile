.PHONY: test lint run dev-run format help

help:
	@echo "Available commands:"
	@echo "  run         Run the production server"
	@echo "  dev-run     Run the server in development mode"
	@echo "  test        Run all tests"
	@echo "  lint        Run linter (flake8)"
	@echo "  format      Format code (black)"

run:
	python3 run_ui.py

dev-run:
	OPERATIONAL_SAFE_MODE=true python3 run_ui.py

test:
	PYTHONPATH=. python3 -m pytest

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

format:
	black .
