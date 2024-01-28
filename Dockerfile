# syntax=docker/dockerfile:1
FROM python:3.9

WORKDIR /app 

COPY requirements.txt requirements.txt

RUN pip3 install itsdangerous==2.0.1 && \
    apt-get update && \
    apt-get install -y apt-file vim && \
    apt-file update && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x /app/container_start_server.sh 

CMD /app/container_start_server.sh

