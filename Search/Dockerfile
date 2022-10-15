FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /search

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 3000

COPY . ./

RUN pip install pipenv

RUN pipenv install --deploy --system
