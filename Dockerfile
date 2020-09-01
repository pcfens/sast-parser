FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

CMD ["python", "parse-sast.py"]