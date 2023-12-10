# syntax=docker/dockerfile:1
FROM python:3.9


WORKDIR /app 
COPY . .

RUN pip3 install itsdangerous==2.0.1 && \
    apt-get update && \
    apt-get install -y apt-file vim && \
    apt-file update && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt install nodejs npm -y

RUN npm -v
RUN npm cache clean -f && \
    npm install -g n && \
    n stable
RUN npm install -g newman

RUN pip3 install -r requirements.txt

RUN chmod +x /app/container_start_server.sh 

CMD /app/container_start_server.sh 