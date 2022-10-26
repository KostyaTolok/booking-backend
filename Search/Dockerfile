FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /search

RUN pip install pipenv

COPY ./Pipfile /Pipfile

COPY ./Pipfile.lock /Pipfile.lock

RUN pipenv install --deploy --system

COPY ./entrypoint.prod.sh /entrypoint.prod.sh
RUN chmod +x /entrypoint.prod.sh
ENTRYPOINT ["/entrypoint.prod.sh"]

EXPOSE 3000

COPY . ./
