FROM python:3.6-alpine

RUN adduser -D fish

WORKDIR /home/fish

RUN apk add build-base
RUN apk add libffi
RUN apk add libffi-dev
RUN apk add openssl-dev

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app.py enter_domains.py create_user.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R fish:fish ./
USER fish

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
