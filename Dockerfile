# Docker image for python interpreter
FROM python:3.7

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python"]
CMD ["-m microblog.py"]