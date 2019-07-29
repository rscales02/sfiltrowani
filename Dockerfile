FROM python:3.6.6-alpine3.6

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
RUN python -m venv env
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev openssl-dev
RUN env/bin/pip install -U pip
RUN env/bin/pip install -r requirements.txt
RUN env/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
#something to commit
