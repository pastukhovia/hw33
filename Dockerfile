FROM python:3.10-slim

EXPOSE 8000

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY todolist/requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . .