# Build:

.PHONY: build
build:
	@which pipenv || pip3 install pipenv
	@pipenv install

.PHONY: build-dev
build-dev:
	make build
	@pipenv install --dev

.PHONY: generate-checkstyle-config
generate-checkstyle-config:
	@pipenv run pylint --generate-rcfile > .pylintrc

.PHONY: install-checkstyle-githooks
install-checkstyle-githooks:
	@pip3 install pre-commit
	pre-commit install

.PHONY: uninstall-checkstyle-githooks
uninstall-checkstyle-githooks:
	pre-commit uninstall


# Test

.PHONY: test
test:
	@pipenv run python3 -m unittest

.PHONY: test-coverage
test-coverage:
	@pipenv run coverage3 run --branch --source=. --omit="tests/*" --data-file=".coverage" -m unittest
	@pipenv run coverage3 xml --data-file=".coverage" -o "coverage.xml"
	@pipenv run coverage3 report --data-file=".coverage" --show-missing

.PHONY: test-debug
test-debug:
	@pipenv run python3 -m pdb -m unittest

.PHONY: checkstyle
checkstyle:
	@pipenv run pycodestyle --max-line-length=120 src/ tests/
	@pipenv run pylint src/ tests/


# Run

.PHONY: run-dev
run-dev:
	@pipenv run python3 -m flask --app src/app run
