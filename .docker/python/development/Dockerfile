FROM tiangolo/uwsgi-nginx-flask:python3.8

EXPOSE 8080

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
