FROM python:3.12-alpine

ENV URIPARSER_HOME=/opt/uriparser
ENV URIPARSER_USER=uriparser

# Install general dependencies
RUN apk update && apk upgrade
RUN pip install pipenv

# Install URI Parser REST API
RUN adduser -Ds /bin/sh ${URIPARSER_USER} \
    && mkdir -p ${URIPARSER_HOME}

COPY Pipfile ${URIPARSER_HOME}/Pipfile
COPY Pipfile.lock ${URIPARSER_HOME}/Pipfile.lock
COPY app.py ${URIPARSER_HOME}
COPY config.toml ${URIPARSER_HOME}
COPY uri_parser/ ${URIPARSER_HOME}/uri_parser/

# NOTE: To install only production dependencies remove the "--dev" flag from the below "pipenv install" command!
#RUN PIPENV_PIPFILE=${URIPARSER_HOME}/Pipfile pipenv install --system --deploy
RUN PIPENV_PIPFILE=${URIPARSER_HOME}/Pipfile pipenv install --dev --system --deploy

USER ${URIPARSER_USER}
WORKDIR ${URIPARSER_HOME}

# Run URI Parser REST API
#EXPOSE 5000
#CMD ["python3", "-m" , "flask", "--app", "app", "run", "--host=0.0.0.0"]
EXPOSE 8000
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=4", "app:app"]
