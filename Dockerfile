FROM python:alpine

ADD VERSION .

COPY requirements.txt /tmp
WORKDIR /tmp
RUN apk add --no-cache openssl-dev libffi-dev git make gcc g++ openldap-dev zlib-dev build-base jpeg-dev\
    && pip install pyOpenSSL Pillow\
    && pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD flask run --no-debugger --host=0.0.0.0 --port=5000