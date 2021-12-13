FROM python:latest
MAINTAINER Sabu@gc.team

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]