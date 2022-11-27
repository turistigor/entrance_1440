all:
	poetry run python main.py

sim:
	poetry run python3 src/simulator.py

test:
	poetry run python -m pytest -s tests
