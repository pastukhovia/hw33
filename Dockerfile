FROM python:3.10-slim

EXPOSE 8000

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . .