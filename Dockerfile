# Docker image for python interpreter
FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENV NAME sfiltrowani

CMD ['python -m', 'microblog.py']