FROM debian:stable-slim

WORKDIR /app

RUN apt update && apt upgrade \
&& apt install -y libmariadb-dev libmariadb3 \
&& apt install -y python3-pip \
&& apt install -y nodejs npm

COPY requirements.txt ./
COPY package.json package-lock.json ./

RUN pip install -r requirements.txt \
&& npm ci --no-audit --no-fund --verbose \

COPY . /app/