FROM python:3.7-slim-bullseye

ARG BUILD_DATE

LABEL \
  maintainer="Logan Marchione <logan@loganmarchione.com>" \
  org.opencontainers.image.authors="Logan Marchione <logan@loganmarchione.com>" \
  org.opencontainers.image.title="docker-speedtest-influxdb" \
  org.opencontainers.image.description="Runs Ookla's Speedtest CLI program in Docker, sends the results to InfluxDB" \
  org.opencontainers.image.created=$BUILD_DATE

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg2 \
    tzdata && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8E61C2AB9A6D1557 && \
    apt-get update && \
    curl -s https://install.speedtest.net/app/cli/install.deb.sh | bash && \
    apt-get update && apt-get install speedtest && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --system speedtest

USER speedtest

WORKDIR /usr/scr/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY speedtest.py .

COPY VERSION /

CMD ["python", "-u", "./speedtest.py"]
