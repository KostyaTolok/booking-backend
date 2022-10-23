FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /search

RUN pip install pipenv

COPY ./Pipfile /Pipfile

COPY ./Pipfile.lock /Pipfile.lock

RUN pipenv install --deploy --system

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 3000

COPY . ./
