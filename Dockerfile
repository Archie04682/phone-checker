FROM python:latest
MAINTAINER snowborodist@gmail.com

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]