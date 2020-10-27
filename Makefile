init:
	pip install -r requirements.txt
	pip install .
test:
	python -m pytest tests
ci:
	make test
lint:
	python -m flake8 src/foreman/ --ignore=E501,F401,E203,E128,E402,E731,F821,E712,W503,F811
format:
	black src/foreman
	black tests/
	make lint
sort:
	isort tests
	isort src/foreman
coverage:
	python -m pytest --cov-report term --cov-report xml --cov=src/foreman tests/
	python -m coveralls
show:
	python -m pytest --cov-report term --cov-report html --cov=src/foreman tests/
cov:
	python -m pytest --cov-report term --cov-report xml --cov=src/foreman tests/
publish:
	make format
	make lint
	make test
	python setup.py sdist
	twine upload dist/*
	rm -fr build dist .egg masonite_foreman.egg-info
	rm -rf dist/*
pub:
	python setup.py sdist
	twine upload dist/*
	rm -fr build dist .egg masonite_foreman.egg-info
	rm -rf dist/*
pypirc:
	cp .pypirc ~/.pypirc
