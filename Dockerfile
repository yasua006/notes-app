FROM python:3.11.15-trixie

WORKDIR /app

RUN apt update -y && apt upgrade -y \
&& apt install -y libmariadb-dev libmariadb3 \
&& apt install -y nodejs npm

COPY requirements.txt ./
COPY package.json package-lock.json ./

RUN pip install -r requirements.txt \
&& npm ci --no-audit --no-fund --verbose

COPY . .

RUN ls

CMD ["python", "-m", "uvicorn", "main:asgi_app", "--host", "0.0.0.0"]
