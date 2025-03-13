DOCKER_FILE :=  docker/Dockerfile
DOCKER_IMAGE := uriparser
DOCKER_TAG := latest


# Build:

.PHONY: build
build:
	@which pipenv || pip3 install pipenv
	@pipenv install

.PHONY: build-dev
build-dev:
	make build
	@pipenv install --dev

.PHONY: build-docker
build-docker:
	@docker build -f ${DOCKER_FILE} -t ${DOCKER_IMAGE}:${DOCKER_TAG} .

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

.PHONY: test-docker
test-docker:
	@docker run --name ${DOCKER_IMAGE} --rm -w /opt/uriparser -v $(PWD)/tests:/opt/uriparser/tests ${DOCKER_IMAGE}:${DOCKER_TAG} python3 -m unittest

.PHONY: test-debug
test-debug:
	@pipenv run python3 -m pdb -m unittest

.PHONY: checkstyle
checkstyle:
	@pipenv run pycodestyle --max-line-length=120 app.py uri_parser/ tests/
	@pipenv run pylint app.py uri_parser/ tests/


# Run

.PHONY: run-dev
run-dev:
	@pipenv run python3 -m flask --app app run

.PHONY: run
run:
	@pipenv run gunicorn --workers=4 app:app

.PHONY: run-docker
run-docker:
#	@docker run -p 127.0.0.1:5000:5000 --name ${DOCKER_IMAGE} -it --rm ${DOCKER_IMAGE}:${DOCKER_TAG}
	@docker run -p 127.0.0.1:8000:8000 --name ${DOCKER_IMAGE} -it --rm ${DOCKER_IMAGE}:${DOCKER_TAG}
