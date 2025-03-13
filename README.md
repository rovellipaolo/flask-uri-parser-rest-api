URI Parser REST API
===================

URI Parser REST API is a simple Flask-based REST API to parse URIs.

[![Build Status: GitHub Actions](https://github.com/rovellipaolo/flask-uri-parser-rest-api/actions/workflows/ci.yml/badge.svg)](https://github.com/rovellipaolo/flask-uri-parser-rest-api/actions)
[![Test Coverage: Coveralls](https://coveralls.io/repos/github/rovellipaolo/flask-uri-parser-rest-api/badge.svg)](https://coveralls.io/github/rovellipaolo/flask-uri-parser-rest-api)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


## Overview

URI Parser REST API uses `urllib` (https://docs.python.org/3/library/urllib.html) and `validator` (https://pypi.org/project/validators/) to parse a given URI and extract its parts.

**NOTE: This is just a playground to play with Python/Flask, nothing serious.**


## Build

The first step is cloning the URI Parser REST API repository, or downloading its source code.

```shell
$ git clone https://github.com/rovellipaolo/flask-uri-parser-rest-api
$ cd flask-uri-parser-rest-api
```

To execute URI Parser REST API in your local machine, you need `Python 3.12` or higher installed.
Just launch the following commands, which will install all the needed Python dependencies.

```shell
$ make build-dev
$ make run-dev
```
```shell
$ curl -X GET http://127.0.0.1:5000/api/status
{"message":"REST API up and running... long live and prosper!"}

$ curl -X POST http://127.0.0.1:5000/api/parse -d '{"uri": "https://user:password@domain.tld:8080/path?key=value#fragment"}'
{"fragment":"fragment","host":"domain.tld","path":"/path","port":8080,"query":"key=value","raw":"https://user:password@domain.tld:8080/path?key=value#fragment","scheme":"https","userinfo":"user:password"}
```
**NOTE:** The OpenAPI definition will be exposed at `http://localhost:5000` (Swagger UI) and `http://localhost:5000/openapi.json` (raw JSON).


## Test

Once you've configured it (see the _"Build"_ section), you can also run the tests and checkstyle as follows.

```shell
$ make test
$ make checkstyle
```

You can also run the tests with coverage by launching the following command:
```shell
$ make test-coverage
```

And/or configure the checkstyle to run automatically at every git commit by launching the following command:
```shell
$ make install-githooks
```




## Licence

URI Parser REST API is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
