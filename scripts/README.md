##To install and configure kafka cluster, please follow the steps below:

##This script installs 1 zookeeper server, 2 kafka brokers, 1 producer and 1 consumer on separate VMs.

Update /etc/ansible/hosts file to update ip address, username, ssh key file for each VM

Update the private ip address and hostnames of all VMs in `parameters.json' file

Update zookeeper installation details in config file `zk-common.json`. This file will be used to install Zookeeper servers.

Update zookeeper server config details in config file `zk-1.json`

Update kafka installation details in config files `kafka-common.json`. This file will be used to install Kafka on Kafka broker, producer and consumer VMs

Update kafka broker details in config files `kafka-1.json` and `kafka-2.json`.

Update kafka topic details in `kafka-topic.json` file.

Update kafka producer config details in `kafka-producer.json` file.

Update kafka consumer config details in `kafka-consumer.json` file.

To run the script use command `sudo bash install-kafka.sh`
