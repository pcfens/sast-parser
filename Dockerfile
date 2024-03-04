FROM python:3-alpine

ENV PYTHONUNBUFFERED=1

COPY templates/* /app/templates/
COPY entrypoint.sh /app/
COPY parse-sast.py /app/
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt \
    && apk add --no-cache curl

WORKDIR /reports

ENTRYPOINT [ "/app/entrypoint.sh" ]