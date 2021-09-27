FROM python:3-alpine

# add genral command line tooling
RUN apk update
RUN apk add curl
RUN apk add nano

# create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add pyhon dependencies
COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY *.py /usr/src/app/
COPY *.ini /usr/src/app/

CMD ["/bin/sh"]