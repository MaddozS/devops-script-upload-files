#!/bin/bash
nohup bash -c '/usr/share/logstash/bin/logstash -f /app/logstash-simple.conf' & cron -f