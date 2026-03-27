FROM python: 3.14

ENV host=0.0.0.0
ENV port=3306
ENV username=yasua006
ENV password=Skole123
ENV db_name=note_app_db

RUN apt update \
&& apt install -y libmariadb-dev libmariadb3 \
&& npm install && pip install -r requirements.txt

WORKDIR /app

COPY . /app/