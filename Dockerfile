FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
WORKDIR /reports

RUN pip install --no-cache-dir -r /app/requirements.txt \
    && apk add --no-cache curl

COPY . /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]