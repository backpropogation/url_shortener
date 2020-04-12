FROM python:3.7 AS server

RUN apt-get update && \
    apt-get install -y git
RUN apt-get install python3-dev -y

RUN mkdir /server
WORKDIR /server

COPY ./requirements.txt /server/
RUN pip install -r requirements.txt

COPY ./server /server
RUN python ./manage.py collectstatic --noinput

#########################################

FROM nginx:1.13

RUN rm -v /etc/nginx/nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
