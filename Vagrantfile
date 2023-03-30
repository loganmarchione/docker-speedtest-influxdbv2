# -*- mode: ruby -*-
# vi: set ft=ruby :

########################################
# Variables
########################################
v_base = "debian/bullseye64"
v_name = "docker-speedtest-influxdbv2"
v_cpu = 2
v_mem = 1024

########################################
# Configuration
########################################

Vagrant.configure("2") do |config|
  config.vm.box = v_base
  config.vm.define v_name
  config.vm.hostname = v_name

  config.vm.network "private_network", type: "dhcp"
  config.vm.network "forwarded_port", guest: 8086, host: 8086, protocol: "tcp", auto_correct: true
  config.ssh.extra_args = ["-t", "cd /vagrant; bash --login"]

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.name = v_name
    vb.cpus = v_cpu
    vb.memory = v_mem
  end

  # This application needs InfluxDB to run
  # The quickest way to get this is to use Docker (the irony)
  config.vm.provision "docker" do |d|
    d.run "influxdbv2",
      image: "influxdb:2.4-alpine",
      args: "-p 8086:8086 --env DOCKER_INFLUXDB_INIT_MODE=setup --env DOCKER_INFLUXDB_INIT_USERNAME=user1 --env DOCKER_INFLUXDB_INIT_PASSWORD=user1234 --env DOCKER_INFLUXDB_INIT_ORG=my_test_org --env DOCKER_INFLUXDB_INIT_BUCKET=SpeedtestStats --env DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=asdfghjkl"
  end

  config.vm.provision "basics", type: "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y --no-install-recommends apt-transport-https bash build-essential ca-certificates curl git jq rsync software-properties-common unzip vim wget zip
  SHELL

  config.vm.provision "app-development", type: "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y --no-install-recommends python3 python3-pip
    curl -s https://install.speedtest.net/app/cli/install.deb.sh | bash
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://packagecloud.io/ookla/speedtest-cli/gpgkey | gpg --dearmor > /etc/apt/keyrings/ookla_speedtest-cli-archive-keyring.gpg
    apt-get update
    apt-get install -y --no-install-recommends speedtest
  SHELL

  config.vm.provision "versions", type: "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    python3 --version
    pip3 --version
  SHELL

end
