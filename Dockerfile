FROM debian:stable-slim

WORKDIR /app

RUN apt update && apt upgrade \
&& apt install -y libmariadb-dev libmariadb3 \
&& apt install -y nodejs npm \
&& apt install python3-pip

COPY package.json package-lock.json ./
COPY requirements.txt ./

RUN npm ci --no-audit --no-fund --verbose \
&& pip install -r requirements.txt

COPY . /app/