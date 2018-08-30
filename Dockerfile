FROM python:3.6.5-alpine

WORKDIR /usr/src/app

ADD . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "flask", "db", "upgrade" ]

CMD [ "python", "./rapi.py" ]