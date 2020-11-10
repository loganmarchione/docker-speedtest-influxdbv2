FROM python:3.7-slim-buster

ARG BUILD_DATE

LABEL \
  maintainer="Logan Marchione <logan@loganmarchione.com>" \
  org.opencontainers.image.authors="Logan Marchione <logan@loganmarchione.com>" \
  org.opencontainers.image.title="docker-speedtest-influxdb" \
  org.opencontainers.image.description="Runs Ookla's Speedtest CLI program in Docker, sends the results to InfluxDB" \
  org.opencontainers.image.created=$BUILD_DATE

ENV VERSION 1.0.0
ENV ARCH x86_64
ENV PLATFORM linux

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg2 \
    tzdata \
    wget && \
    rm -rf /var/lib/apt/lists/* && \
    wget --quiet --output-document ookla-speedtest-${VERSION}-${ARCH}-${PLATFORM}.deb https://ookla.bintray.com/download/ookla-speedtest-${VERSION}-${ARCH}-${PLATFORM}.deb && \
    apt-get install -y ./ookla-speedtest-${VERSION}-${ARCH}-${PLATFORM}.deb && \
    rm ./ookla-speedtest-${VERSION}-${ARCH}-${PLATFORM}.deb && \
    adduser --system speedtest

USER speedtest

WORKDIR /usr/scr/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY speedtest.py .

COPY VERSION /

CMD ["python", "-u", "./speedtest.py"]
