FROM python:3.7.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN apk --update add python3 py3-pip openssl ca-certificates py3-openssl wget git 
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev build-base
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del build-dependencies


COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]
