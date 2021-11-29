FROM python:3.8.10-slim-buster

RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY crontab /etc/cron.d/crontab
ADD . /app

RUN /usr/bin/crontab /etc/cron.d/crontab
RUN pip install -r requirements.txt
# run crond as main process of container
CMD ["cron", "-f"]