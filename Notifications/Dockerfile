FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY app /app/

CMD ["python", "main.py"]
