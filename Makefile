all: install

install:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

build:
	.venv/bin/python script.py