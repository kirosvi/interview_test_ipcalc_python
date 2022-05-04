FROM python:3.10.4-alpine3.15

WORKDIR /app

RUN adduser -s /bin/ash -D -h /app app

ADD . /app

RUN pip install -r /app/requirements.txt

USER app

CMD /app/main.py
