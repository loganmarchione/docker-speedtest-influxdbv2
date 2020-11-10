# docker-speedtest-influxdbv2

![CI/CD](https://github.com/loganmarchione/docker-speedtest-influxdbv2/workflows/CI/CD/badge.svg)
[![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/loganmarchione/docker-speedtest-influxdbv2)](https://hub.docker.com/r/loganmarchione/docker-speedtest-influxdbv2)
[![MicroBadger Layers](https://img.shields.io/microbadger/layers/loganmarchione/docker-speedtest-influxdbv2)](https://microbadger.com/images/loganmarchione/docker-speedtest-influxdbv2)

Runs Ookla's [Speedtest CLI](https://www.speedtest.net/apps/cli) program in Docker, sends the results to InfluxDB
  - Source code: [GitHub](https://github.com/loganmarchione/docker-speedtest-influxdbv2)
  - Docker container: [Docker Hub](https://hub.docker.com/r/loganmarchione/docker-speedtest-influxdbv2)
  - Image base: [Python (slim Buster)](https://hub.docker.com/_/python)
  - Init system: N/A
  - Application: [Speedtest CLI](https://www.speedtest.net/apps/cli)

## Explanation

  - This runs Ooka's Speedtest CLI program on an interval, then writes the data to an InfluxDB database (you can later graph this data with Grafana or Chronograf)
  - This does **NOT** use the open-source [speedtest-cli](https://github.com/sivel/speedtest-cli). That program uses the Speedtest.net HTTP API. This program uses Ookla's official CLI application.
  - ⚠️ Ookla's speedtest application is closed-source (the binary applications are [here](https://bintray.com/ookla)) and Ookla's reasoning for this decision is [here](https://www.reddit.com/r/HomeNetworking/comments/dpalqu/speedtestnet_just_launched_an_official_c_cli/f5tm9up/) ⚠️
  - ⚠️ Ookla's speedtest application reports all data back to Ookla ⚠️

## Requirements

  - This should work with InfluxDB 2.0, but also with 1.8 using some [compatability APIs](https://github.com/influxdata/influxdb-client-python#influxdb-1-8-api-compatibility) for 2.0.
  - You must already have an InfluxDB database created, along with a user that has `WRITE` and `READ` permissions on that database.
  - This Docker container needs to be able to reach that InfluxDB instance by hostname, IP address, or Docker service name (I run this container on the same Docker network as my InfluxDB instance).
  - ⚠️ Depending on how often you run this, you may need to monitor your internet connection's usage. If you have a data cap, you could exceed it. The standard speedtest uses about 750MB of data per run. See below for an example. ⚠️

```
CONTAINER: NET I/O
speedtest: 225MB / 495MB
```

## Docker image information

### Docker image tags
  - `latest`: Latest version
  - `X.X.X`: [Semantic version](https://semver.org/) (use if you want to stick on a specific version)

### Environment variables
| Variable       | Required?                | Definition                       | Example                                     | Comments                                                                                         |
|----------------|--------------------------|----------------------------------|---------------------------------------------|--------------------------------------------------------------------------------------------------|
| INFLUXDB_HOST  | No (default: localhost)  | Server hosting the InfluxDB      | 'localhost' or your Docker service name     |                                                                                                  |
| INFLUXDB_PORT  | No (default: 8086)       | InfluxDB port                    | 8086                                        |                                                                                                  |
| INFLUXDB_USER  | Yes                      | Database username                | influx_username                             | Needs to have WRITE and READ permissions already                                                 |
| INFLUXDB_PASS  | Yes                      | Database password                | influx_password                             |                                                                                                  |
| INFLUXDB_DB    | Yes                      | Database name                    | SpeedtestStats                              | Must already be created, this does not create a DB                                               |
| SLEEPY_TIME    | No (default: 3600)       | Seconds to sleep between runs    | 3600                                        | The loop takes about 15-30 seconds to run, so I wouldn't set this value any lower than 60 (1min) |

### Ports
N/A

### Volumes
N/A

### Example usage
Below is an example docker-compose.yml file.
```
version: '3'
services:
  speedtest:
    container_name: tig_speedtest
    restart: unless-stopped
    environment:
      - INFLUXDB_HOST=influxdb
      - INFLUXDB_PORT=8086
      - INFLUXDB_USER=influx_username
      - INFLUXDB_PASS=influx_password
      - INFLUXDB_DB=SpeedtestStats
      - SLEEPY_TIME=3600
    networks:
      - influx
    image: loganmarchione/docker-speedtest-influxdbv2:latest

networks:
  influx:
```

## TODO
- [ ] Learn Python
- [x] ~~Run the processes inside the container as a non-root user~~
- [ ] Add a [healthcheck](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [x] ~~Move the database connection check to a function~~
- [ ] Add logic to check if variables are set
- [x] ~~Add defaults for HOST and PORT~~
- [ ] Update CI/CD with tests
- [x] ~~Add warning about bandwidth~~
