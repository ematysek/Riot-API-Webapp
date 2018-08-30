FROM python:3.6.5-alpine

WORKDIR /usr/src/app

ADD . /usr/src/app

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN flask db upgrade

CMD [ "flask", "run", "--host", "0.0.0.0" ]