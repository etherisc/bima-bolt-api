FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

COPY src-gen /usr/src/app
COPY src /usr/src/app

EXPOSE 8181

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]