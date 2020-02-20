FROM python:2.7.17-slim-stretch

RUN apt-get update \
&& apt-get clean && apt-get install vim -y && \
apt-get install nmap -y

RUN mkdir ./opt/usd_convert/
COPY . /opt/usd_convert/

WORKDIR /opt/usd_convert
RUN ls
RUN chmod +x run.sh


CMD /opt/usd_convert/run.sh
