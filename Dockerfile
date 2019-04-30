# base sand box image
FROM python:3.7


# create working directory
WORKDIR /app

# copy current directory into sandbox working directory
COPY . /app

# start virtual environment in container
RUN python -m venv venv
RUN pip install -r requirements.txt
EXPOSE 80
RUN flask run