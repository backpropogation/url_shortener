FROM python:3.7

RUN apt-get update && \
    apt-get install -y git
RUN apt-get install python3-dev -y

RUN mkdir /server
WORKDIR /server

COPY ./requirements.txt /server/
RUN pip install -r requirements.txt

COPY ./server /server
