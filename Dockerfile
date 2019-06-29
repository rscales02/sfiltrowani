# Docker image for python interpreter
FROM python:3.7

WORKDIR /app

COPY . /app

# RUN pip install virtualenv
RUN source env/bin/activate
RUN pip install -r requirements.txt

EXPOSE 80

ENV NAME sfiltrowani

CMD ['python', 'microblog.py']