FROM debian:latest

RUN apt update && apt upgrade \
&& apt install -y libmariadb-dev libmariadb3 \
&& apt install -y nodejs npm \
&& npm install && pip install -r requirements.txt

WORKDIR /app

COPY . /app/