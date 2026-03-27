FROM debian:latest

ENV host=0.0.0.0
ENV port=3306
ENV username=yasua006
ENV password=Skole123
ENV db_name=note_app_db

RUN apt-get update && apt-get upgrade \
&& apt-get install -y libmariadb-dev libmariadb3 \
apt-get install nodejs npm \
&& npm install && pip install -r requirements.txt

WORKDIR /app

COPY . /app/