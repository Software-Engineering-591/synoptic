FROM python:3.12-alpine

RUN apk add --no-cache poetry

WORKDIR /app
# prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED=1

COPY . .
RUN poetry install