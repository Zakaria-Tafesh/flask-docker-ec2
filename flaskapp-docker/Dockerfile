FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y
RUN apt-get install -y \
    libmysqlclient-dev \
    pkg-config

COPY requirements.txt requirements.txt
COPY flaskapp /opt/

RUN pip3 install -r requirements.txt
WORKDIR /opt/

CMD ["gunicorn3", "-b", "0.0.0.0:8888", "app:app", "--workers=5"]
