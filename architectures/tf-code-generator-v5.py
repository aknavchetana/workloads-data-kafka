#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import sys 


# In[ ]:


var=len(sys.argv)
# if var!=2:
#     print("command usage: python filename Excel file")
#     sys.exit()
# EXCEL_INPUT = sys.argv[1]
EXCEL_INPUT = 'Kafka-inventory.xlsx'
EXCEL_SHEET_INVENTORY = "Inventory"
EXCEL_SHEET_VARIABLES = "Variables"
EXCEL_SHEET_OS = "OS"
EXCEL_SHEET_DISK = "Disk"
EXCEL_SHEET_AVAILABILITY_SET = "AvailabilitySet"
EXCEL_SHEET_SECURITY_RULES = "SecurityRules"


# In[ ]:


EXCEL_COL_ENVIRONMENT = "ENVIRONMENT"
EXCEL_COL_RES_GRP_NAME = "RESOURCE-GROUP-NAME"
EXCEL_COL_REGION = "REGION"
EXCEL_COL_LAYER = "LAYER"
EXCEL_COL_SERVICE_TYPE = "SERVICE-TYPE"
EXCEL_COL_RESOURCE_NAME = "RESOURCE-NAME"
EXCEL_COL_PARENT_RESOURCE_NAME = "PARENT-RESOURCE-NAME"
EXCEL_COL_ADDRESS_SPACE = "ADDRESS-SPACE"
EXCEL_COL_ADDRESS_PREFIX = "ADDRESS-PREFIX"
EXCEL_COL_VM_OS = "OS"
EXCEL_COL_VM_SIZE = "VM"
EXCEL_COL_DISK = "DISK"
EXCEL_COL_SRC_RES_NAME = "SOURCE-RESOURCE-NAME"
EXCEL_COL_ENVIRONMENT_TAG ="ENVIRONMENT-TAG"
EXCEL_COL_PROJECT_TAG ="PROJECT-TAG"
EXCEL_COL_DEPARTMENT_TAG ="DEPARTMENT-TAG"
EXCEL_COL_OWNER_TAG ="OWNER-TAG"


# In[ ]:


EXCEL_VAL_VNET = "VNET"
EXCEL_VAL_SUBNET = "SUBNET"
EXCEL_VAL_SECGRP = "SECGRP"
EXCEL_VAL_PUBLIC_IP = "PUBLIC-IP"
EXCEL_VAL_VM = "VM"
EXCEL_VAL_STORAGE = "STORAGE"


# In[ ]:


EXCEL_COL_VM = "VM"
EXCEL_COL_VM_IMAGE_OFFER = "VM-IMAGE-OFFER"
EXCEL_COL_VM_IMAGE_SKU = "VM-IMAGE-SKU"
EXCEL_COL_VM_IMAGE_VERSION = "VM-IMAGE-VERSION"


# In[ ]:


EXCEL_COL_DISK_TYPE = "DISK-TYPE"
EXCEL_COL_DISK_SIZE = "DISK-SIZE"
EXCEL_COL_CACHING_POLICY = "CACHING-POLICY"


# In[ ]:


EXCEL_COL_AV_SET_LAYER = "LAYER"
EXCEL_COL_AV_SET_NAME = "AVAILABILITY-SET-NAME"


# In[ ]:


xls = pd.ExcelFile(EXCEL_INPUT)
df_inv = pd.read_excel(xls, EXCEL_SHEET_INVENTORY)
df_var = pd.read_excel(xls, EXCEL_SHEET_VARIABLES)
df_os = pd.read_excel(xls, EXCEL_SHEET_OS)
df_dsk = pd.read_excel(xls, EXCEL_SHEET_DISK)
df_av = pd.read_excel(xls, EXCEL_SHEET_AVAILABILITY_SET)
df_sec = pd.read_excel(xls, EXCEL_SHEET_SECURITY_RULES)


# In[ ]:


VAR_ADMIN_USERNAME = df_var.loc[df_var['VAR-NAME'] == 'VM-ADMIN-USERNAME']['VALUE'].item()
VAR_ADMIN_PASSWORD = df_var.loc[df_var['VAR-NAME'] == 'VM-ADMIN-PASSWORD']['VALUE'].item()
VAR_PUBLIC_KEY = df_var.loc[df_var['VAR-NAME'] == 'VM-PUBLIC-KEY']['VALUE'].item()
VAR_SUBSCRIPTION_ID = df_var.loc[df_var['VAR-NAME'] == 'TF-SUBSCRIPTION-ID']['VALUE'].item()
VAR_CLIENT_ID = df_var.loc[df_var['VAR-NAME'] == 'TF-CLIENT-ID']['VALUE'].item()
VAR_TENANT_ID = df_var.loc[df_var['VAR-NAME'] == 'TF-TENANT-ID']['VALUE'].item()


# In[ ]:


def codeGenerateResourceGroup(name, location):
    var_resource_group = 'TF_' + name
    str_resource_group = '\nresource "azurerm_resource_group"' + ' "' + var_resource_group + '" {' + '\n' + '\tname = "' + name + '"' + '\n' + '\tlocation = "' + location + '"' + '\n' + '}'
    return var_resource_group, str_resource_group


# In[ ]:


def codeGenerateVnet(name, address_space, var_resource_group,tags):
    var_vnet = 'TF_' + name
    str_vnet = '\n\nresource "azurerm_virtual_network"' + ' "' + var_vnet + '" {' + '\n' + '\tname = "' + name + '"' + '\n' + '\taddress_space = ["' + address_space + '"]\n' + '\tlocation = ' + 'azurerm_resource_group.' + var_resource_group + '.location' + '\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' +codegeneratetag(tags)+'\n'+'}'
    return var_vnet, str_vnet


# In[ ]:


def codeGenerateSubnet(name, var_resource_group, var_vnet, address_prefix,tags):
    var_subnet = 'TF_' + name
    str_subnet = '\n\nresource "azurerm_subnet"' + ' "' + var_subnet + '" {' + '\n' + '\tname = "' + name + '"' + '\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' + '\tvirtual_network_name = ' + 'azurerm_virtual_network.' + var_vnet + '.name' + '\n' + '\taddress_prefixes = ["' + address_prefix + '"]\n' +codegeneratetag(tags)+'\n'+'}'
    return var_subnet, str_subnet


# In[ ]:


def codeGenerateSecurityGroup(name, var_resource_group):
    var_sec_grp = 'TF_' + name
    str_sec_grp = '\n\nresource "azurerm_network_security_group"' + ' "' + var_sec_grp + '" {' + '\n' + '\tname = "' + name + '"' + '\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' + '\tlocation = ' + 'azurerm_resource_group.' + var_resource_group + '.location' + '\n' + '\tsecurity_rule {\n' + '\t\taccess = "Allow"\n' + '\t\tdirection = "Inbound"\n' + '\t\tname = "tls"\n' + '\t\tpriority = 100\n' + '\t\tprotocol = "Tcp"\n' + '\t\tsource_port_range = "*"\n' + '\t\tsource_address_prefix = "*"\n' + '\t\tdestination_port_range = "*"\n' + '\t\tdestination_address_prefix = "*"\n\t}' + '\n}'
#     print(str_sec_grp)
    return var_sec_grp, str_sec_grp


# In[ ]:


def codeGeneratePublicip(name, var_resource_group,tags):
    var_pip = 'TF_' + name
    str_pip = '\n\nresource "azurerm_public_ip"' + ' "' + var_pip + '" {' + '\n' + '\tname = "' + name + '"' + '\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' + '\tlocation = ' + 'azurerm_resource_group.' + var_resource_group + '.location' + '\n' + '\tallocation_method = "Dynamic"\n' +codegeneratetag(tags)+'\n'+'}'
    return var_pip, str_pip


# In[ ]:


def codeGenerateNetworkInterface(name, var_resource_group, var_subnet, var_pip='', public_ip=False):
    var_nic_lst = []
    str_nic_lst = []
    if(public_ip):
        nic_name = 'NIC_EXT_' + name
        var_nic = 'TF_' + nic_name
        str_public_ip = '\t\tpublic_ip_address_id = azurerm_public_ip.' + var_pip + '.id\n'
        str_nic = '\n\nresource "azurerm_network_interface"' + ' "' + var_nic + '" {' + '\n' + '\tname = "' + nic_name + '"' + '\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' + '\tlocation = ' + 'azurerm_resource_group.' + var_resource_group + '.location' + '\n\n' + '\tip_configuration { \n\t\tname = "internal"\n' + '\t\tsubnet_id = azurerm_subnet.' + var_subnet + '.id\n' + '\t\tprivate_ip_address_allocation = "Dynamic"\n' + str_public_ip + '\t}\n' +'}'
        var_nic_lst.append(var_nic)
        str_nic_lst.append(str_nic)
    nic_name = 'NIC_INT_' + name
    var_nic = 'TF_' + nic_name
    str_nic = '\n\nresource "azurerm_network_interface"' + ' "' + var_nic + '" {' + '\n' + '\tname = "' + nic_name + '"' + '\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' + '\tlocation = ' + 'azurerm_resource_group.' + var_resource_group + '.location' + '\n\n' + '\tip_configuration { \n\t\tname = "internal"\n' + '\t\tsubnet_id = azurerm_subnet.' + var_subnet + '.id\n' + '\t\tprivate_ip_address_allocation = "Dynamic"\n' + '\t}\n' + '}'
    var_nic_lst.append(var_nic)
    str_nic_lst.append(str_nic)
    return var_nic_lst, str_nic_lst


# In[ ]:


def codeGenerateVm(name, var_resource_group, vm_os, vm_size, admin_username, admin_password, var_nic_lst, var_public_key):
    var_vm = 'TF_' + name
    str_var_nic = ''
    if vm_os == 'SUSE':
        str_disable_auth = '\tdisable_password_authentication = true\n'
        str_vm_os = 'linux'
        str_vm_name = name
    elif vm_os == 'WINDOWS':
        str_disable_auth = ''
        str_vm_os = 'windows'
        str_vm_name = name[-15:]
    elif vm_os == 'LINUX':
        str_disable_auth = '\tdisable_password_authentication = true\n'
        str_vm_os = 'linux'
        str_vm_name = name    
    for var_nic in var_nic_lst:
        str_var_nic += '\t\tazurerm_network_interface.' + var_nic + '.id,\n'
    str_vm = '\n\nresource "azurerm_'+ str_vm_os + '_virtual_machine" "' + var_vm + '" {\n' + '\tname = "' + str_vm_name + '"\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' + '\tlocation = ' + 'azurerm_resource_group.' + var_resource_group + '.location' + '\n' + '\tsize = "' + vm_size + '"\n' + '\tadmin_username = "' + admin_username + '"\n'  + str_disable_auth + '\tadmin_ssh_key {\n\t\tusername = "azureadmin"\n\t\tpublic_key = file("' + var_public_key + '")\n\t}'+ '\n\tnetwork_interface_ids = [\n' + str_var_nic + '\t]\n' 
    return var_vm, str_vm


# In[ ]:


def codeGenerateOsImage(vm_os, vm_image_offer, vm_image_sku, vm_image_version):
    if vm_os == 'WINDOWS':
        vm_publisher = 'MicrosoftWindowsServer'
    elif vm_os == 'SUSE':
        vm_publisher = 'Suse'
    elif vm_os == 'LINUX':
        vm_publisher = 'Canonical'    
    str_vm_image = '\n\tsource_image_reference {\n\t\tpublisher   = "' + vm_publisher + '"\n\t\toffer = "' + vm_image_offer + '"\n\t\tsku = "' + vm_image_sku + '"\n\t\tversion = "' + vm_image_version + '"\n\t}'
    return str_vm_image


# In[ ]:


def codeGenerateManagedDisk(name, var_resource_group, storage_type,  disk_size,tags,caching='', is_root = False):
    var_disk = 'TF_' + name
    str_additional_info = ''
    if is_root:
        str_disk = '\n\n\tos_disk {\n' + '\t\tstorage_account_type = "' + storage_type + '"\n'  + '\t\tdisk_size_gb = ' + str(disk_size) + '\n\t\tcaching = "' + caching + '"\n\t}' +'\n'+codegeneratetag(tags)+'\n'+'}'
    else:
        str_disk = '\n\nresource "azurerm_managed_disk" "' + var_disk + '" {\n' + '\tname = "' + name + '"\n' + '\tresource_group_name = ' + 'azurerm_resource_group.' + var_resource_group + '.name' + '\n' + '\tlocation = ' + 'azurerm_resource_group.' + var_resource_group + '.location' + '\n\tstorage_account_type = "' + storage_type + '"\n'  + '\tdisk_size_gb = ' + str(disk_size) + '\n\tcreate_option = "Empty"\n'+codegeneratetag(tags)+'\n'+'}\n'
#     print(str_disk)
    return var_disk, str_disk


# In[ ]:


def codeGenerateDiskAttach(disk_name, vm_name, lun, caching, vm_os):
    var_disk_attach = 'disk-attach-' + str(lun)
    if vm_os == 'WINDOWS':
        vm_type = 'windows'
    elif vm_os == 'SUSE':
        vm_type = 'linux'
    str_disk_attach = 'resource "azurerm_virtual_machine_data_disk_attachment" "' + var_disk_attach + '" {\n' + '\tmanaged_disk_id = azurerm_managed_disk.' + disk_name + '.id\n' + '\tvirtual_machine_id = azurerm_' + vm_type + '_virtual_machine.' + vm_name + '.id\n' + '\tlun = "' + str(lun) + '"\n' + '\tcaching = "' + caching + '"\n'+'}'
    return var_disk_attach, str_disk_attach


# In[ ]:


def codeGenerateAvailSet(name, var_resource_group):
    var_av_set = 'TF_' + name
    str_av_set = '\n\nresource "azurerm_availability_set" "' + var_av_set + '" {\n' + '\tname = "' + name + '"\n' + '\tlocation = azurerm_resource_group.' + var_resource_group + '.location\n' + '\tresource_group_name = azurerm_resource_group.' + var_resource_group + '.name\n}'
    return var_av_set, str_av_set


# In[ ]:


def codegeneratetag(tags):
    tags = [str(x) for x in tags]
    chcklist=len(set(tags)) == 1
    if chcklist==False:
        str_tag='\ttags = { '+'\n'+'\t\t'
        lst=['environment','project','department','owner']
        for tag,l in zip(tags,lst):
            if tag != 'nan':
                str_tag = str_tag+l+" = "+'"'+tag+'"'+"\n\t\t"
        str_tag=str_tag+'\n\t'+'}'
        return str_tag
    else:
        str_tag=''
        return str_tag


# In[ ]:


def showNetworkView(df, var_resource_group, tf_code_str):
    df_vnet = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VNET]
    df_vm = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM]
    
    vm_dict = {}
    vm_nic = {}
    vm_pip = {}
    
    print("---NETWORK-VIEW--")
    print("-----------------")
    for iter_vnet, vnet_row in df_vnet.iterrows():
        
        #vnet
        vnet_name = str(vnet_row[EXCEL_COL_RESOURCE_NAME])
        address_space = str(vnet_row[EXCEL_COL_ADDRESS_SPACE])
        vnet_tags=[vnet_row[EXCEL_COL_ENVIRONMENT_TAG],vnet_row[EXCEL_COL_PROJECT_TAG],vnet_row[EXCEL_COL_DEPARTMENT_TAG],vnet_row[EXCEL_COL_OWNER_TAG]]
        res_vnet_group = codeGenerateVnet(vnet_name, address_space, var_resource_group,vnet_tags)
        tf_code_str += res_vnet_group[1]
        print("VNET" + "=" + vnet_name)
        
        ext_subnet = {}
        
        #subnet
        df_subnet = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_SUBNET) & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == vnet_name)]
        for iter_subnet, subnet_row in df_subnet.iterrows():
            subnet_name = str(subnet_row[EXCEL_COL_RESOURCE_NAME])
            address_prefix = str(subnet_row[EXCEL_COL_ADDRESS_PREFIX])
            subnet_tags=[subnet_row[EXCEL_COL_ENVIRONMENT_TAG],subnet_row[EXCEL_COL_PROJECT_TAG],subnet_row[EXCEL_COL_DEPARTMENT_TAG],subnet_row[EXCEL_COL_OWNER_TAG]]
            res_subnet_group = codeGenerateSubnet(subnet_name, var_resource_group, res_vnet_group[0], address_prefix,subnet_tags)
            tf_code_str += res_subnet_group[1]
            print("\tSubnet" + "=" + subnet_name)
            
            #secgrps
            df_secgrp = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_SECGRP) & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == subnet_name)]
            for iter_secgrp, secgrp_row in df_secgrp.iterrows():
                secgrp_name = secgrp_row[EXCEL_COL_RESOURCE_NAME]
                res_sec_group = codeGenerateSecurityGroup(secgrp_name, var_resource_group)
                tf_code_str += res_sec_group[1]
                print("\t\tSecurity Group: " + secgrp_name)
                
                #public-ip
                df_pip = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_PUBLIC_IP)  & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == secgrp_name)]
                for iter_row, pip_row in df_pip.iterrows():
                    pip_name = pip_row[EXCEL_COL_RESOURCE_NAME]
                    pip_tags=[pip_row[EXCEL_COL_ENVIRONMENT_TAG],pip_row[EXCEL_COL_PROJECT_TAG],pip_row[EXCEL_COL_DEPARTMENT_TAG],pip_row[EXCEL_COL_OWNER_TAG]]
                    res_pip = codeGeneratePublicip(pip_name, var_resource_group,pip_tags)
                    tf_code_str += res_pip[1]                   
                    ext_subnet[subnet_name] = res_pip
                    print("\t\t\tPublic IP: " + pip_name)
            
            #vm
            df_vm = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM) & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == subnet_name)]
            for iter_vm, vm_row in df_vm.iterrows():
                vm_name = vm_row[EXCEL_COL_RESOURCE_NAME]
                vm_size = 'Standard_' + vm_row[EXCEL_COL_VM_SIZE]
                vm_os = vm_row[EXCEL_COL_VM_OS]
                
        
                #nic-ext-and-int
                if subnet_name in ext_subnet:
                    res_pip = ext_subnet[subnet_name]
                    res_nic_lst = codeGenerateNetworkInterface(vm_name, var_resource_group, res_subnet_group[0], var_pip=res_pip[0], public_ip=True)
                    for res_nic in res_nic_lst[1]:
                        tf_code_str += res_nic
                    vm_nic[vm_name] = res_nic_lst[0]
                    vm_pip[vm_name] = res_pip[0]
                        
                #nic-int    
                else:
                    res_nic_lst = codeGenerateNetworkInterface(vm_name, var_resource_group, res_subnet_group[0])
                    tf_code_str += res_nic_lst[1][0]
                res_vm = codeGenerateVm(vm_name, var_resource_group, vm_os, vm_size, VAR_ADMIN_USERNAME, VAR_ADMIN_PASSWORD, res_nic_lst[0], VAR_PUBLIC_KEY)    
                vm_dict[vm_name] = res_vm
                print("\t\t\tVM: " + vm_name)

                
                
    print("-----------------")
    return tf_code_str, vm_dict, vm_nic, vm_pip


# In[ ]:


def showComputeView(df, df_av, var_resource_group, tf_code_str, vm_dict):
    df_vm = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM]
    df_storage = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_STORAGE]

    print("--COMPUTE-VIEW--")
    print("----------------")
    
    av_lst = {}

    for iter_avset, avset_row in df_av.iterrows():
        avset_layer = avset_row[EXCEL_COL_AV_SET_LAYER]
        avset_name = avset_row[EXCEL_COL_AV_SET_NAME]
        res_avset = codeGenerateAvailSet(avset_name, var_resource_group)
        av_lst[avset_layer] = res_avset[0]
        tf_code_str += res_avset[1]

    for iter_vm, vm_row in df_vm.iterrows():
        vm_name = vm_row[EXCEL_COL_RESOURCE_NAME]
        vm_os = vm_row[EXCEL_COL_VM_OS]
        print("VM: " + vm_name)
        
        vm_layer = vm_row[EXCEL_COL_LAYER]
        
        res_str_vm = ''
        res_str_vm += vm_dict[vm_name][1]
        
        if vm_layer in av_lst:
            str_av_set_id = '\n\tavailability_set_id = azurerm_availability_set.' + av_lst[vm_layer] + '.id\n'
            res_str_vm += str_av_set_id
    
        lun = 1
        
        storage_rows = df_storage.loc[df_storage[EXCEL_COL_PARENT_RESOURCE_NAME] == vm_name]
        for iter_storage, storage_row in storage_rows.iterrows():
            disk_name = storage_row[EXCEL_COL_RESOURCE_NAME]
            disk = storage_row[EXCEL_COL_DISK]
            vm_tags=[vm_row[EXCEL_COL_ENVIRONMENT_TAG],vm_row[EXCEL_COL_PROJECT_TAG],vm_row[EXCEL_COL_DEPARTMENT_TAG],vm_row[EXCEL_COL_OWNER_TAG]]
            storage_tags=[storage_row[EXCEL_COL_ENVIRONMENT_TAG],storage_row[EXCEL_COL_PROJECT_TAG],storage_row[EXCEL_COL_DEPARTMENT_TAG],storage_row[EXCEL_COL_OWNER_TAG]]
            print("\tDisk Name: " + disk_name)
            disk_info = df_dsk.loc[df_dsk[EXCEL_COL_DISK] == disk]
            disk_type = disk_info[EXCEL_COL_DISK_TYPE].item()
            disk_size = disk_info[EXCEL_COL_DISK_SIZE].item()
            caching_policy = disk_info[EXCEL_COL_CACHING_POLICY].item()
            
        
            if(disk_name[-4:] == "ROOT"):
                os_info = df_os.loc[df_os[EXCEL_COL_VM] == vm_os]
                vm_image_offer = os_info[EXCEL_COL_VM_IMAGE_OFFER].item()
                vm_image_sku =  os_info[EXCEL_COL_VM_IMAGE_SKU].item()
                vm_image_version =  os_info[EXCEL_COL_VM_IMAGE_VERSION].item()

                res_os_image = codeGenerateOsImage(vm_os, vm_image_offer, vm_image_sku, vm_image_version)
                res_str_vm += res_os_image
                
                res_os_disk = codeGenerateManagedDisk(disk_name, var_resource_group, disk_type, disk_size,vm_tags,caching_policy, True)
                res_str_vm += res_os_disk[1]
            
            else:  
                res_disk = codeGenerateManagedDisk(disk_name, var_resource_group, disk_type, disk_size,storage_tags)
                tf_code_str += res_disk[1]
                res_disk_attach = codeGenerateDiskAttach(res_disk[0], vm_dict[vm_name][0], lun, caching_policy, vm_os)
                tf_code_str += res_disk_attach[1]
                lun += 1
        tf_code_str += res_str_vm
                
    print("------------------------------------------------------------------------------------------------------")
    return tf_code_str


# In[ ]:


def codeGenerateInternalDRComponents(var_pri_res_group, var_sec_res_group, var_dr_names, tf_code_str):
    #     var_rs_vault = 'vault'
    str_rs_vault = '\nresource "azurerm_recovery_services_vault" "' + var_dr_names['var_rs_vault'] + '" {\n\tname = "example-recovery-vault"\n\tlocation = azurerm_resource_group.' + var_sec_res_group + '.location\n\tresource_group_name = azurerm_resource_group.' + var_sec_res_group + '.name\n\tsku = "Standard"\n}'
    #     print(str_rs_vault)
    tf_code_str += str_rs_vault

    #     var_time_delay = 'wait_120_seconds'
    str_time_delay = '\nresource "time_sleep" "' + var_dr_names['var_time_delay'] + '" {\n\tdepends_on = [azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + ']\n\tcreate_duration = "120s"\n\tdestroy_duration = "30s"\n}'
    #print(str_time_delay)
    tf_code_str += str_time_delay

    #     var_primary_fab = 'primary'
    str_primary_fab = '\nresource "azurerm_site_recovery_fabric" "' + var_dr_names['var_primary_fab'] + '" {\n\tname = "primary-fabric"\n\tresource_group_name = azurerm_resource_group.' + var_sec_res_group + '.name\n\trecovery_vault_name = azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + '.name\n\tlocation = azurerm_resource_group.' + var_pri_res_group + '.location\n\tdepends_on = [time_sleep.' + var_dr_names['var_time_delay'] + ']\n}'
    #     print(str_primary_fab)
    tf_code_str += str_primary_fab

    #     var_secondary_fab = 'secondary'
    str_secondary_fab = '\nresource "azurerm_site_recovery_fabric" "' + var_dr_names['var_secondary_fab'] + '" {\n\tname = "secondary-fabric"\n\tresource_group_name = azurerm_resource_group.' + var_sec_res_group + '.name\n\trecovery_vault_name = azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + '.name\n\tlocation = azurerm_resource_group.' + var_sec_res_group + '.location\n\tdepends_on = [time_sleep.' + var_dr_names['var_time_delay'] + ']\n}'
    #     print(str_secondary_fab)
    tf_code_str += str_secondary_fab

    #     var_primary_cont = 'primary'
    str_primary_cont = '\nresource "azurerm_site_recovery_protection_container" "' + var_dr_names['var_primary_cont'] + '" {\n\tname = "primary-protection-container"\n\tresource_group_name  = azurerm_resource_group.' + var_sec_res_group + '.name\n\trecovery_vault_name  = azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + '.name\n\trecovery_fabric_name = azurerm_site_recovery_fabric.' + var_dr_names['var_primary_fab'] + '.name\n\tdepends_on = [azurerm_site_recovery_fabric.' + var_dr_names['var_primary_fab'] + ']\n}'
    #     print(str_primary_cont)
    tf_code_str +=  str_primary_cont

    #     var_secondary_cont = 'secondary'
    str_secondary_cont = '\nresource "azurerm_site_recovery_protection_container" "' + var_dr_names['var_secondary_cont'] + '" {\n\tname = "secondary-protection-container"\n\tresource_group_name  = azurerm_resource_group.' + var_sec_res_group + '.name\n\trecovery_vault_name  = azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + '.name\n\trecovery_fabric_name = azurerm_site_recovery_fabric.' + var_dr_names['var_secondary_fab'] + '.name\n\tdepends_on = [azurerm_site_recovery_fabric.' + var_dr_names['var_secondary_fab'] + ']\n}'
    #     print(str_secondary_cont) 
    tf_code_str += str_secondary_cont

    #     var_policy = 'policy'
    str_policy = '\nresource "azurerm_site_recovery_replication_policy" "' + var_dr_names['var_policy'] + '" {\n\tname = "policy"\n\tresource_group_name = azurerm_resource_group.' + var_sec_res_group + '.name\n\trecovery_vault_name = azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + '.name\n\trecovery_point_retention_in_minutes = 24 * 60\n\tapplication_consistent_snapshot_frequency_in_minutes = 4 * 60\n\tdepends_on = [time_sleep.' + var_dr_names['var_time_delay'] + ']\n}'
    #     print(str_policy)
    tf_code_str += str_policy

    #     var_cont_mapping = 'container_mapping'
    str_cont_mapping = '\nresource "azurerm_site_recovery_protection_container_mapping" "' + var_dr_names['var_cont_mapping'] + '" {\n\tname = "container-mapping"\n\tresource_group_name = azurerm_resource_group.' + var_sec_res_group + '.name\n\trecovery_vault_name = azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + '.name\n\trecovery_fabric_name = azurerm_site_recovery_fabric.' + var_dr_names['var_primary_fab'] + '.name\n\trecovery_source_protection_container_name = azurerm_site_recovery_protection_container.' + var_dr_names['var_primary_cont'] + '.name\n\trecovery_target_protection_container_id = azurerm_site_recovery_protection_container.' + var_dr_names['var_secondary_cont'] + '.id\n\trecovery_replication_policy_id = azurerm_site_recovery_replication_policy.' + var_dr_names['var_policy'] + '.id\n\tdepends_on = [\n\t\tazurerm_site_recovery_protection_container.primary,\n\t\tazurerm_site_recovery_protection_container.' + var_dr_names['var_secondary_cont'] + ',\n\t\tazurerm_site_recovery_replication_policy.' + var_dr_names['var_policy'] + '\n\t]\n}'
    #     print(str_cont_mapping)
    tf_code_str += str_cont_mapping

    #     var_storage_acnt = 'primary'
    str_storage_acnt = '\nresource "azurerm_storage_account" "' + var_dr_names['var_storage_acnt'] + '" {\n\tname = "primarystact"\n\tlocation =  azurerm_resource_group.' + var_pri_res_group + '.location\n\tresource_group_name =  azurerm_resource_group.' + var_pri_res_group + '.name\n\taccount_tier = "Standard"\n\taccount_replication_type = "LRS"\n}'
    #     print(str_storage_acnt) 
    tf_code_str += str_storage_acnt

#     print(tf_code_str)
    return tf_code_str


# In[ ]:



def codeGenerateRepVM(df, var_resource_group, var_dr_names, tf_code_str, vm_nic, vm_pip):
    df_vnet = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VNET]
    df_vm = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM]
 
    for iter_vnet, vnet_row in df_vnet.iterrows():
        
        #vnet
        vnet_name = str(vnet_row[EXCEL_COL_RESOURCE_NAME])
        var_vnet_name = 'TF_' + vnet_name
        df_subnet = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_SUBNET) & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == vnet_name)]
        for iter_subnet, subnet_row in df_subnet.iterrows():    
            subnet_name = str(subnet_row[EXCEL_COL_RESOURCE_NAME])
            #vm
            df_vm = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM) & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == subnet_name)]
            for iter_vm, vm_row in df_vm.iterrows():
                vm_name = vm_row[EXCEL_COL_RESOURCE_NAME]
                str_vm_name = vm_name[-15:]
                var_vm_name = 'TF_' + vm_name 
                src_vm_name = 'TF_' + vm_row[EXCEL_COL_SRC_RES_NAME]
                
                str_rep_vm_pt_1 = '\n\nresource "azurerm_site_recovery_replicated_vm" "' + var_vm_name + '" {\n\tname = "' + str_vm_name + '"\n\tresource_group_name = azurerm_resource_group.' + var_sec_res_group + '.name\n\trecovery_vault_name = azurerm_recovery_services_vault.' + var_dr_names['var_rs_vault'] + '.name\n\tsource_recovery_fabric_name = azurerm_site_recovery_fabric.' + var_dr_names['var_primary_fab'] + '.name\n\tsource_vm_id = azurerm_virtual_machine.' + src_vm_name + '.id\n\trecovery_replication_policy_id = azurerm_site_recovery_replication_policy.' + var_dr_names['var_policy'] + '.id\n\tsource_recovery_protection_container_name = azurerm_site_recovery_protection_container.' + var_dr_names['var_primary_cont'] + '.name\n\ttarget_resource_group_id = azurerm_resource_group.' + var_sec_res_group + '.id\n\ttarget_recovery_fabric_id = azurerm_site_recovery_fabric.' + var_dr_names['var_secondary_cont'] + '.id\n\ttarget_recovery_protection_container_id = azurerm_site_recovery_protection_container.' +  var_dr_names['var_secondary_cont'] + '.id\n\n\tmanaged_disk {\n\t\tdisk_id = azurerm_virtual_machine.' + src_vm_name + '.storage_os_disk[0].managed_disk_id\n\t\tstaging_storage_account_id = azurerm_storage_account.' + var_dr_names['var_storage_acnt'] + '.id\n\t\ttarget_resource_group_id   = azurerm_resource_group.' + var_sec_res_group + '.id\n\t\ttarget_disk_type = "Premium_LRS"\n\t\ttarget_replica_disk_type = "Premium_LRS"\n\t}\n\n\ttarget_network_id = azurerm_virtual_network.' + var_vnet_name + '.id\n'
                for nic in vm_nic[ vm_row[EXCEL_COL_SRC_RES_NAME]]:
                    str_pub_ip = '\n\t\trecovery_public_ip_address_id = azurerm_public_ip.' + vm_pip[vm_row[EXCEL_COL_SRC_RES_NAME]] + '.id' if nic.find('EXT') > -1 else ''
                    str_nic = '\n\n\tnetwork_interface {\n\t\tsource_network_interface_id = azurerm_network_interface.' + nic + '.id + \n\t\ttarget_subnet_name = "' + subnet_name + '"' + str_pub_ip + '\n\t}'
                    str_rep_vm_pt_1 += str_nic
#                     print('\n-----------------\n\n' + str_nic_pt_1 + '\n\n----------------------------------\n')
                str_rep_vm_pt_2 = '\n\n\tdepends_on = [azurerm_site_recovery_protection_container_mapping.' + var_dr_names['var_cont_mapping'] + ']\n}'
                str_rep_vm_pt_1 += str_rep_vm_pt_2
                tf_code_str += str_rep_vm_pt_1
#                 print(str_vm_rep)
    return tf_code_str


# In[ ]:


def showDisasterRecoveryView(df, var_pri_res_group, var_sec_res_group, tf_code_str, vm_nic, vm_pip):
    var_dr_names = {'var_rs_vault' : 'vault', 'var_time_delay' : 'wait_120_seconds', 'var_primary_fab' : 'primary', 'var_secondary_fab' : 'secondary', 'var_primary_cont' : 'primary', 'var_secondary_cont' : 'secondary', 'var_policy' : 'policy', 'var_cont_mapping' : 'container_mapping', 'var_storage_acnt' : 'primary'}
    tf_code_str = codeGenerateInternalDRComponents(var_pri_res_group, var_sec_res_group, var_dr_names, tf_code_str)
    tf_code_str = codeGenerateRepVM(df, var_sec_res_group, var_dr_names, tf_code_str, vm_nic, vm_pip)
    return tf_code_str


# In[ ]:


tf_code_str = 'terraform {\n\trequired_providers {\n\t\tazurerm = {\n\t\t\tsource = "hashicorp/azurerm"\n\t\t\tversion = "=2.73.0"\n\t\t}\n\t}\n}\n\nprovider "azurerm" {\n\tfeatures {}\n\n\tuse_msi = true\n\n\tsubscription_id = "' + VAR_SUBSCRIPTION_ID + '"\n\tclient_id = "' + VAR_CLIENT_ID + '"\n\ttenant_id = "' + VAR_TENANT_ID + '"\n}\n'

def mandatory_check(lstr_net):
#     rname=str(VAR_RESOURCE_GROUP_NAME)
    aname=str(VAR_ADMIN_USERNAME)
    pname=str(VAR_ADMIN_PASSWORD)
#     if rname=='nan':
#         s='Resource Group name is missing'
#         lstr_net.append(s)
    if aname=='nan':
        s='Username is missing'
        lstr_net.append(s)
    if pname=='nan':
        s='Password is missing'
        lstr_net.append(s)
    
    df_inv_list = [d for _, d in df_inv.groupby([EXCEL_COL_REGION])]
    for df in df_inv_list:
        #vnet
        df_vnet = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VNET]
        df_vm = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM]
        for iter_vnet, vnet_row in df_vnet.iterrows():
            vnet_name = str(vnet_row[EXCEL_COL_RESOURCE_NAME])
            address_space = str(vnet_row[EXCEL_COL_ADDRESS_SPACE])
            if vnet_name == 'nan':
                s = 'VNET name missing in ' #+ rname
                lstr_net.append(s)
            if address_space == 'nan':
                s = 'VNET address space missing in '# + rname
                lstr_net.append(s)
        #subnet
        df_subnet = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_SUBNET) & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == vnet_name) ]
        for iter_subnet, subnet_row in df_subnet.iterrows():
            subnet_name = str(subnet_row[EXCEL_COL_RESOURCE_NAME])
            address_prefix = str(subnet_row[EXCEL_COL_ADDRESS_PREFIX])
            if subnet_name == 'nan':
                s = 'SUBNET name missing in ' + vnet_name
                lstr_net.append(s)
            if address_prefix == 'nan':
                s = 'SUBNET address prefix missing in ' + vnet_name
                lstr_net.append(s)
            #secgrps
            df_secgrp = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_SECGRP)& (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == subnet_name)]
            for iter_secgrp, secgrp_row in df_secgrp.iterrows():
                secgrp_name = str(secgrp_row[EXCEL_COL_RESOURCE_NAME])
                if secgrp_name == 'nan':
                    s = 'SECURITY_GRP name missing in ' + subnet_name
                    lstr_net.append(s)
                #public-ip
                df_pip = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_PUBLIC_IP) & (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == secgrp_name)]
                for iter_row, pip_row in df_pip.iterrows():
                    pip_name = str(pip_row[EXCEL_COL_RESOURCE_NAME])
                    if pip_name == 'nan':
                        s = 'PUBLIC_IP name missing in ' + secgrp_name
                        lstr_net.append(s)
            #vm
            df_vm = df_inv[(df_inv[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM)& (df_inv[EXCEL_COL_PARENT_RESOURCE_NAME] == subnet_name)]
            for iter_vm, vm_row in df_vm.iterrows():
                vm_name =str(vm_row[EXCEL_COL_RESOURCE_NAME])
                vm_size = str(vm_row[EXCEL_COL_VM_SIZE])
                vm_os = str(vm_row[EXCEL_COL_VM_OS])
                if vm_name=='nan':
                    s='VM_NAME missing in '+subnet_name
                    lstr_net.append(s)
                if vm_size=='nan':
                    s='VM_SIZE missing in '+vm_name
                    lstr_net.append(s)
                if vm_os=='nan':
                    s='VM_OS missing in '+vm_name
                    lstr_net.append(s)
        df_vm = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_VM]
        df_storage = df[df[EXCEL_COL_SERVICE_TYPE] == EXCEL_VAL_STORAGE]
        for iter_vm, vm_row in df_vm.iterrows():
            vm_name = str(vm_row[EXCEL_COL_RESOURCE_NAME])
            vm_os = str(vm_row[EXCEL_COL_VM_OS])
            storage_rows = df_storage.loc[df_storage[EXCEL_COL_PARENT_RESOURCE_NAME] == vm_name]
            for iter_storage, storage_row in storage_rows.iterrows():
                disk_name = str(storage_row[EXCEL_COL_RESOURCE_NAME])
                disk = str(storage_row[EXCEL_COL_DISK])
                if disk_name=='nan':
                    s='Disk Name missing in '+vm_name
                    lstr_net.append(s)
                if disk=='nan':
                    s='Disk Type missing in '+ disk_name
                    lstr_net.append(s)
                if disk!='nan':
                    disk_info = df_dsk.loc[df_dsk[EXCEL_COL_DISK] == disk]
                    disk_type = disk_info[EXCEL_COL_DISK_TYPE].item()
                    disk_size = disk_info[EXCEL_COL_DISK_SIZE].item()
                    caching_policy = disk_info[EXCEL_COL_CACHING_POLICY].item()
                    
                    if str(disk_type)=='nan':
                        s='Disk type missing in '+ disk
                        lstr_net.append(s)
                    if str(disk_size)=='nan':
                        s='Disk Size missing in '+ disk
                        lstr_net.append(s)
                    if str(caching_policy)=='nan':
                        s='Caching Policy missing in '+ disk
                        lstr_net.append(s)
                if vm_os!='nan':
                    if(disk_name[-4:] == "ROOT"):
                        os_info = df_os.loc[df_os[EXCEL_COL_VM] == vm_os]
                        vm_image_offer = os_info[EXCEL_COL_VM_IMAGE_OFFER].item()
                        vm_image_sku =  os_info[EXCEL_COL_VM_IMAGE_SKU].item()
                        vm_image_version =  os_info[EXCEL_COL_VM_IMAGE_VERSION].item()
                        if str(vm_image_offer)=='nan':
                            s='Vm_image_Offer missing in '+vm_name
                            lstr_net.append(s)
                        if str(vm_image_sku)=='nan':
                            s='Vm_Image_Sku missing in '+ vm_name
                            lstr_net.append(s)
                        if str(vm_image_version)=='nan':
                            s='Vm_Image_Version missing in '+ vm_name
                            lstr_net.append(s)
    return lstr_net    

lstr_net=[]

lstr_net=mandatory_check(lstr_net)
if len(lstr_net)!=0:
    for item in lstr_net:
        print(item)
    sys.exit()
else:
    print("1.Display Components \n2.Display tf-code\n3.Save the code in file\n")
    option=int(input("Enter your choice[1/2/3]: "))

#     df_inv_list = [d for _, d in df_inv.groupby([EXCEL_COL_REGION])]
    df_inv_list = [d for _, d in df_inv.groupby([EXCEL_COL_ENVIRONMENT], sort = False)]
#     print(df_inv_list)
#     i = 0
    var_pri_res_group = ''
    var_sec_res_group = ''
    var_pri_vm_nic = {}
    var_pri_vm_pip = {}
    for df in df_inv_list:
        environment = df[EXCEL_COL_ENVIRONMENT].iloc[0]
        location = df[EXCEL_COL_REGION].iloc[0]
        name = df[EXCEL_COL_RES_GRP_NAME].iloc[0]
        res_resource_group = codeGenerateResourceGroup(name, location)
        tf_code_str += res_resource_group[1]
        if environment == 'PROD':
            print("----------------")
            print("--PROD--")
            print("----------------")
            tf_code_str, vm_dict, vm_nic, vm_pip = showNetworkView(df, res_resource_group[0], tf_code_str)
            var_pri_res_group = res_resource_group[0]
            var_pri_vm_nic = vm_nic
            var_pri_vm_pip = vm_pip
            tf_code_str = showComputeView(df, df_av, res_resource_group[0], tf_code_str, vm_dict)
        elif environment == 'DR':
            print("----------------")
            print("--DISASTER-RECOVERY--")
            print("----------------")
            tf_code_str, vm_dict, vm_nic, vm_pip = showNetworkView(df, res_resource_group[0], tf_code_str)
            var_sec_res_group = res_resource_group[0]
            tf_code_str = showDisasterRecoveryView(df, var_pri_res_group, var_sec_res_group, tf_code_str, var_pri_vm_nic, var_pri_vm_pip)
            
    if option==2:
        print(tf_code_str)
    elif option==3:
        fname = input("Enter the file name with .tf extension : ")
        f = open(fname, 'w')
        f.write(tf_code_str)
        f.close()
        print("Terraform code is generated successfully!")


# In[ ]:





# In[ ]:




