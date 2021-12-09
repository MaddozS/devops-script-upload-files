FROM python:3.8.10-slim-buster

RUN apt-get update && apt-get -y install cron

WORKDIR /app

# Install required pacakges.
RUN apt-get update && apt-get install -y \
    wget \
    gnupg

# Logstash install preparation.
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list

# Install logstash.
RUN apt-get update && apt-get install -y \
    logstash

COPY crontab /etc/cron.d/crontab
ADD . /app

RUN /usr/bin/crontab /etc/cron.d/crontab
RUN pip install -r requirements.txt
# run crond as main process of container
CMD [ "bash", "start.sh" ]