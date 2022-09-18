FROM python:3.10.4-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/event_management_system /app

WORKDIR /app
VOLUME sqlite-data:/app/db

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]