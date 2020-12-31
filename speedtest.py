#!/usr/bin/env python3

import datetime
import json
import os
import subprocess
import time
import socket
import sys
from influxdb_client import InfluxDBClient

# Variables
influxdb_host = os.getenv("INFLUXDB_HOST", "localhost")
influxdb_port = int(os.getenv("INFLUXDB_PORT", 8086))
influxdb_user = os.getenv("INFLUXDB_USER")
influxdb_pass = os.getenv("INFLUXDB_PASS")
influxdb_db = os.getenv("INFLUXDB_DB")
sleepy_time = int(os.getenv("SLEEPY_TIME", 3600))
start_time = datetime.datetime.utcnow().isoformat()
default_hostname = socket.gethostname()
hostname = os.getenv("SPEEDTEST_HOST", default_hostname)


def db_check():
    print("STATE: Running database check")
    client_health = client.health().status

    if client_health == "pass":
        print("STATE: Connection", client_health)
    elif client_health == "fail":
        print("ERROR: Connection", client_health, " - Check host, port, user, pass")
        sys.exit(1)
    else:
        print("ERROR: Something else went wrong")
        sys.exit(1)


def speedtest():
    db_check()

    current_time = datetime.datetime.utcnow().isoformat()
    print("STATE: Loop running at", current_time)

    # Run Speedtest
    print("STATE: Speedtest running")
    my_speed = subprocess.run(['/usr/bin/speedtest', '--accept-license', '--accept-gdpr', '--format=json'], stdout=subprocess.PIPE, text=True, check=True)

    # Convert the string into JSON, only getting the stdout and stripping the first/last characters
    my_json = json.loads(my_speed.stdout.strip())

    # Get the values from JSON and log them to the Docker logs
    # Basic values
    speed_down = my_json["download"]["bandwidth"]
    speed_up = my_json["upload"]["bandwidth"]
    ping_latency = my_json["ping"]["latency"]
    ping_jitter = my_json["ping"]["jitter"]
    result_url = my_json["result"]["url"]
    # Advanced values
    speedtest_server_id = my_json["server"]["id"]
    speedtest_server_name = my_json["server"]["name"]
    speedtest_server_location = my_json["server"]["location"]
    speedtest_server_country = my_json["server"]["country"]
    speedtest_server_host = my_json["server"]["host"]

    # Print results to Docker logs
    print("NOTE:  RESULTS ARE SAVED IN BPS NOT MBPS")
    print("STATE: Your download     ", speed_down, "bps")
    print("STATE: Your upload       ", speed_up, "bps")
    print("STATE: Your ping latency ", ping_latency, "ms")
    print("STATE: Your ping jitter  ", ping_jitter, "ms")
    print("STATE: Your server info  ", speedtest_server_id, speedtest_server_name, speedtest_server_location, speedtest_server_country, speedtest_server_host)
    print("STATE: Your URL is       ", result_url, " <--- This is not saved to InfluxDB")

    # This is ugly, but trying to get output in line protocol format (UNIX time is appended automatically)
    # https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/
    p = "speedtest," + "service=speedtest.net," + "host=" + str(hostname) + " download=" + str(speed_down) + ",upload=" + str(speed_up) + ",ping_latency=" + str(ping_latency) + ",ping_jitter=" + str(ping_jitter) + ",speedtest_server_id=" + str(speedtest_server_id) + ",speedtest_server_name=" + "\"" + str(speedtest_server_name) + "\"" + ",speedtest_server_location=" + "\"" + str(speedtest_server_location) + "\"" + ",speedtest_server_country=" + "\"" + str(speedtest_server_country) + "\"" + ",speedtest_server_host=" + "\"" + str(speedtest_server_host) + "\""

    try:
        print("STATE: Writing to database")
        write_api = client.write_api()
        write_api.write(bucket=influxdb_db, record=p)
        write_api.__del__()
    except Exception as err:
        print("ERROR: Error writing to database")
        print(err)

    print("STATE: Sleeping for", sleepy_time, "seconds")
    time.sleep(sleepy_time)


# Some logging
print("#####\nScript starting!\n#####")
print("STATE: Starting at", start_time)
print("STATE: Sleep time between runs set to", sleepy_time, "seconds")

# Check if variables are set
print("STATE: Checking environment variables...")
if 'INFLUXDB_DB' in os.environ:
    pass
else:
    print("ERROR: INFLUXDB_DB is not set")
    sys.exit(1)

if 'INFLUXDB_USER' in os.environ:
    pass
else:
    print("ERROR: INFLUXDB_USER is not set")
    sys.exit(1)

if 'INFLUXDB_PASS' in os.environ:
    pass
else:
    print("ERROR: INFLUXDB_PASS is not set")
    sys.exit(1)

# Instantiate the connection
print("STATE: Connecting to InfluxDB...")
connection_string = "http://" + influxdb_host + ":" + str(influxdb_port)
client = InfluxDBClient(url=connection_string, token=f'{influxdb_user}:{influxdb_pass}', org='-')

while True:
    speedtest()
