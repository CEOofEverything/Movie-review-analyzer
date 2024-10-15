FROM python:3.10
WORKDIR /app
RUN apt-get update -y
RUN apt-get upgrade -y
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./review_analyzer ./review_analyzer
CMD gunicorn -w 3 --chdir ./review_analyzer review_analyzer.wsgi --bind 0.0.0.0:8000
