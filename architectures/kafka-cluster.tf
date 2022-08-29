terraform {
	required_providers {
		azurerm = {
			source = "hashicorp/azurerm"
			version = "=2.73.0"
		}
	}
}

provider "azurerm" {
	features {}

	use_msi = true

	subscription_id = "b0387326-5e31-4f92-a146-178320a8d6b5"
	client_id = "6492975e-35e0-42d7-a0dd-756181a499f3"
	tenant_id = "7833d61b-a185-4f1b-8ea2-cf1f9d35de5e"
}

resource "azurerm_resource_group" "TF_Kafka_RSGrp" {
	name = "Kafka_RSGrp"
	location = "eastus2"
}

resource "azurerm_virtual_network" "TF_HT_VIRTUAL_NETWORK" {
	name = "HT_VIRTUAL_NETWORK"
	address_space = ["12.1.0.0/16"]
	location = azurerm_resource_group.TF_Kafka_RSGrp.location
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name

}

resource "azurerm_subnet" "TF_HT_CLUSTER_SUB_NETWORK" {
	name = "HT_CLUSTER_SUB_NETWORK"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	virtual_network_name = azurerm_virtual_network.TF_HT_VIRTUAL_NETWORK.name
	address_prefixes = ["12.1.1.0/24"]

}

resource "azurerm_network_interface" "TF_NIC_INT_HT-VM-ZK-1" {
	name = "NIC_INT_HT-VM-ZK-1"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location

	ip_configuration { 
		name = "internal"
		subnet_id = azurerm_subnet.TF_HT_CLUSTER_SUB_NETWORK.id
		private_ip_address_allocation = "Dynamic"
	}
}

resource "azurerm_network_interface" "TF_NIC_INT_HT-VM-KAFKA-1" {
	name = "NIC_INT_HT-VM-KAFKA-1"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location

	ip_configuration { 
		name = "internal"
		subnet_id = azurerm_subnet.TF_HT_CLUSTER_SUB_NETWORK.id
		private_ip_address_allocation = "Dynamic"
	}
}

resource "azurerm_network_interface" "TF_NIC_INT_HT-VM-KAFKA-2" {
	name = "NIC_INT_HT-VM-KAFKA-2"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location

	ip_configuration { 
		name = "internal"
		subnet_id = azurerm_subnet.TF_HT_CLUSTER_SUB_NETWORK.id
		private_ip_address_allocation = "Dynamic"
	}
}

resource "azurerm_network_interface" "TF_NIC_INT_HT-VM-PRODUCER" {
	name = "NIC_INT_HT-VM-PRODUCER"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location

	ip_configuration { 
		name = "internal"
		subnet_id = azurerm_subnet.TF_HT_CLUSTER_SUB_NETWORK.id
		private_ip_address_allocation = "Dynamic"
	}
}

resource "azurerm_network_interface" "TF_NIC_INT_HT-VM-CONSUMER" {
	name = "NIC_INT_HT-VM-CONSUMER"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location

	ip_configuration { 
		name = "internal"
		subnet_id = azurerm_subnet.TF_HT_CLUSTER_SUB_NETWORK.id
		private_ip_address_allocation = "Dynamic"
	}
}

resource "azurerm_linux_virtual_machine" "TF_HT-VM-ZK-1" {
	name = "HT-VM-ZK-1"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location
	size = "Standard_d4ds_v4"
	admin_username = "azureadmin"
	disable_password_authentication = true
	admin_ssh_key {
		username = "azureadmin"
		public_key = file("~/.ssh/id_kafka_cluster.pub")
	}
	network_interface_ids = [
		azurerm_network_interface.TF_NIC_INT_HT-VM-ZK-1.id,
	]

	source_image_reference {
		publisher   = "Canonical"
		offer = "UbuntuServer"
		sku = "18.04-LTS"
		version = "latest"
	}

	os_disk {
		storage_account_type = "Premium_LRS"
		disk_size_gb = 32
		caching = "ReadWrite"
	}
	tags = { 
		environment = "DEV"
		project = "INTEL"
		department = "ACCOUNT"
		owner = "DEVELOPER"
		
	}
}

resource "azurerm_linux_virtual_machine" "TF_HT-VM-KAFKA-1" {
	name = "HT-VM-KAFKA-1"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location
	size = "Standard_d4ds_v4"
	admin_username = "azureadmin"
	disable_password_authentication = true
	admin_ssh_key {
		username = "azureadmin"
		public_key = file("~/.ssh/id_kafka_cluster.pub")
	}
	network_interface_ids = [
		azurerm_network_interface.TF_NIC_INT_HT-VM-KAFKA-1.id,
	]

	source_image_reference {
		publisher   = "Canonical"
		offer = "UbuntuServer"
		sku = "18.04-LTS"
		version = "latest"
	}

	os_disk {
		storage_account_type = "Premium_LRS"
		disk_size_gb = 32
		caching = "ReadWrite"
	}
	tags = { 
		environment = "DEV"
		project = "INTEL"
		department = "ACCOUNT"
		owner = "DEVELOPER"
		
	}
}

resource "azurerm_linux_virtual_machine" "TF_HT-VM-KAFKA-2" {
	name = "HT-VM-KAFKA-2"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location
	size = "Standard_d4ds_v4"
	admin_username = "azureadmin"
	disable_password_authentication = true
	admin_ssh_key {
		username = "azureadmin"
		public_key = file("~/.ssh/id_kafka_cluster.pub")
	}
	network_interface_ids = [
		azurerm_network_interface.TF_NIC_INT_HT-VM-KAFKA-2.id,
	]

	source_image_reference {
		publisher   = "Canonical"
		offer = "UbuntuServer"
		sku = "18.04-LTS"
		version = "latest"
	}

	os_disk {
		storage_account_type = "Premium_LRS"
		disk_size_gb = 32
		caching = "ReadWrite"
	}
	tags = { 
		environment = "DEV"
		project = "INTEL"
		department = "ACCOUNT"
		owner = "DEVELOPER"
		
	}
}

resource "azurerm_linux_virtual_machine" "TF_HT-VM-PRODUCER" {
	name = "HT-VM-PRODUCER"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location
	size = "Standard_d4ds_v4"
	admin_username = "azureadmin"
	disable_password_authentication = true
	admin_ssh_key {
		username = "azureadmin"
		public_key = file("~/.ssh/id_kafka_cluster.pub")
	}
	network_interface_ids = [
		azurerm_network_interface.TF_NIC_INT_HT-VM-PRODUCER.id,
	]

	source_image_reference {
		publisher   = "Canonical"
		offer = "UbuntuServer"
		sku = "18.04-LTS"
		version = "latest"
	}

	os_disk {
		storage_account_type = "Premium_LRS"
		disk_size_gb = 32
		caching = "ReadWrite"
	}
	tags = { 
		environment = "DEV"
		project = "INTEL"
		department = "ACCOUNT"
		owner = "DEVELOPER"
		
	}
}

resource "azurerm_linux_virtual_machine" "TF_HT-VM-CONSUMER" {
	name = "HT-VM-CONSUMER"
	resource_group_name = azurerm_resource_group.TF_Kafka_RSGrp.name
	location = azurerm_resource_group.TF_Kafka_RSGrp.location
	size = "Standard_d4ds_v4"
	admin_username = "azureadmin"
	disable_password_authentication = true
	admin_ssh_key {
		username = "azureadmin"
		public_key = file("~/.ssh/id_kafka_cluster.pub")
	}
	network_interface_ids = [
		azurerm_network_interface.TF_NIC_INT_HT-VM-CONSUMER.id,
	]

	source_image_reference {
		publisher   = "Canonical"
		offer = "UbuntuServer"
		sku = "18.04-LTS"
		version = "latest"
	}

	os_disk {
		storage_account_type = "Premium_LRS"
		disk_size_gb = 32
		caching = "ReadWrite"
	}
	tags = { 
		environment = "DEV"
		project = "INTEL"
		department = "ACCOUNT"
		owner = "DEVELOPER"
		
	}
}