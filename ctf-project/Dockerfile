FROM python:3.9-alpine

RUN apk add bash gcc musl-dev mysql mariadb-dev build-base

ADD requirements.txt /requirements.txt
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir /www

ADD www /www

EXPOSE 8888

ENTRYPOINT [ "/entrypoint.sh" ]
