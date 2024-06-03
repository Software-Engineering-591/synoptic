FROM python:3.12-alpine

RUN apk add --no-cache poetry geos gdal 

WORKDIR /app
# prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY ./prod_requirements.txt .
RUN pip install -r prod_requirements.txt

COPY . .