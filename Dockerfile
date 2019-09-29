FROM alpine:3.7

LABEL org.label-schema.vcs-url="https://github.com/hrbotfi/holidaygen"

RUN apk add --no-cache uwsgi-python3 python3

RUN mkdir -p /usr/src/app
RUN addgroup -S holidaygen && adduser -S -G holidaygen holidaygen

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

USER holidaygen
EXPOSE 5000

CMD [ "uwsgi", "--socket", "0.0.0.0:5000", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--protocol", "http", \
               "--wsgi", "wsgi:application" ]