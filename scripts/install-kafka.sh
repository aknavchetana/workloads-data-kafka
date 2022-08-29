#!/bin/bash

echo "\n\nRunnig Prerequisite tasks on all hosts\n\n"
sudo ansible-playbook prereq.yml -e "@parameters.json" -vvv

echo "\n\nInstalling Zookeeper on Zookeeper Node\n\n"
sudo ansible-playbook zookeeper-install.yml -e "@zk-common.json" -vvv

echo "\n\nConfiguring Zookeeper on Zookeeper Node\n\n"
sudo ansible-playbook zookeeper-configure.yml -e  "@zk-1.json" -vvv

echo "\n\nRunning Zookeeper Server on Zookeeper Node\n\n"
sudo ansible-playbook zookeeper-run.yml -e  "@zk-1.json" -vvv

echo "\n\nInstalling Kafka Broker on Kafka Broker, Producer and Consumer Nodes\n\n"
sudo ansible-playbook kafka-install.yml -e "@kafka-1.json" -vvv

echo "\n\nConfiguring Kafka broker on First Kafka Broker Node\n\n"
sudo ansible-playbook kafka-configure.yml -e "@kafka-1.json" -vvv

echo "\n\nRunning Kafka broker on First Kafka Broker Node\n\n"
sudo ansible-playbook kafka-run.yml -e "@kafka-1.json" -vvv

echo "\n\nConfiguring Kafka broker on Second Kafka Broker Node\n\n"
sudo ansible-playbook kafka-configure.yml -e "@kafka-2.json" -vvv

echo "\n\nRunning Kafka broker on Second Kafka Broker Node\n\n"
sudo ansible-playbook kafka-run.yml -e "@kafka-2.json" -vvv

echo "\n\nCreate Topics on a Kafka Broker Node\n\n"
sudo ansible-playbook kafka-create-topic.yml -e "@kafka-topic.json" -vvv

echo "\n\nStart Producer on Producer Node\n\n"
sudo ansible-playbook kafka-start-producer.yml -e  "@kafka-producer.json" -vvv

echo "\n\nStart Consumer on Consumer Node\n\n"
sudo ansible-playbook kafka-start-consumer.yml -e "@kafka-consumer.json" -vvv
