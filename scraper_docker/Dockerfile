FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install python3-pip -y

COPY requirements.txt requirements.txt
COPY scraper_2023 /opt/

RUN pip3 install -r requirements.txt
WORKDIR /opt/

CMD ["python3", "scraper_2023/main.py"]
