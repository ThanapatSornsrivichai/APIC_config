import json
import csv
from csv import writer
import os.path
import re
import requests 
import urllib3
import pandas as pd
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Open File
with open('ce2_DailyBackupToServer-2020-05-07T00-00-27_1.json') as json_file:
      data = json.load(json_file)
      
#Inventory
#list Inventory
inventory = []
list_inventory_id = []
list_inventory_role = []
list_inventory_name = []
list_inventory_pod = []
list_inventory_sn =[]
list_inventory_oobv4 = []

#CLASS FOR Inventory
class Inventory:
    def __init__(self,id,role,name,pod,sn,oonv4):   
        self.id = id
        self.role = role
        self.name = name
        self.pod = pod
        self.sn = sn
        self.oonv4 = oonv4
        
for x in data["polUni"]["children"][32]["ctrlrInst"]["children"][4]["fabricNodeIdentPol"]["children"]:
    inventory_id = ''
    inventory_role = ''
    inventory_name = ''
    inventory_pod = ''
    inventory_sn = ''
    
    if x.get('fabricNodeIdentP') is not None:
        inventory_id =  x["fabricNodeIdentP"]["attributes"]["nodeId"]
        inventory_role = x["fabricNodeIdentP"]["attributes"]["role"]
        inventory_name = x["fabricNodeIdentP"]["attributes"]["name"]
        inventory_pod = x["fabricNodeIdentP"]["attributes"]["podId"]
        inventory_sn = x["fabricNodeIdentP"]["attributes"]["serial"]
        inventory.append(Inventory(inventory_id,inventory_role,inventory_name,inventory_pod,inventory_sn,''))

for y in data["polUni"]["children"][6]["fvTenant"]["children"][1]["mgmtMgmtP"]["children"][0]["mgmtOoB"]["children"]:
    inventory_oobv4 = ''
 
    if y.get('mgmtRsOoBStNode') is not None:
        #topology/pod-1/node-1201
        fullstring = y["mgmtRsOoBStNode"]["attributes"]["tDn"]
        for check_oobv4 in range(len(inventory)):
            #1201
            substring = inventory[check_oobv4].id
            if substring in fullstring:
                inventory[check_oobv4].oonv4 = y["mgmtRsOoBStNode"]["attributes"]["addr"]


for x in range(len(inventory)):
    list_inventory_id.append(inventory[x].id)
    list_inventory_role.append(inventory[x].role)
    list_inventory_name.append(inventory[x].name)
    list_inventory_pod.append(inventory[x].pod)
    list_inventory_sn.append(inventory[x].sn)
    list_inventory_oobv4.append(inventory[x].oonv4)

#Switch Profile
#list SPF
spf = []
list_spf_name = []
list_spf_des = []
list_spf_types = []
list_spf_selector = []
list_spf_from_node =[]
list_spf_to_node = []
#CLASS FOR BD
class SPF:
    def __init__(self,name,des,types,selector,from_node,to_node):   
        self.name = name
        self.des = des
        self.types = types
        self.selector = selector
        self.from_node = from_node
        self.to_node = to_node

count = int(len(data["polUni"]["children"][22]["infraInfra"]["children"]))
for x in range(count):
    spf_name = ''
    spf_des = ''
    spf_types = ''
    spf_selector = ''
    spf_from_node = ''
    spf_to_node = ''
    if data["polUni"]["children"][22]["infraInfra"]["children"][x].get('infraSpineP') is not None:
        spf_name = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP']["attributes"]["name"]
        spf_des = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP']["attributes"]["descr"]
        spf_types = 'Spine'
        if data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP'].get('children') is not None:
            if data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP']["children"][0].get('infraSpineS') is not None:
                spf_selector = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP']["children"][0]["infraSpineS"]["attributes"]["name"]  
                if data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP']["children"][0]["infraSpineS"]["children"][1].get('infraNodeBlk') is not None:
                    spf_from_node = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP']["children"][0]["infraSpineS"]["children"][1]["infraNodeBlk"]["attributes"]["from_"]  
                    spf_to_node =   data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraSpineP']["children"][0]["infraSpineS"]["children"][1]["infraNodeBlk"]["attributes"]["to_"] 
        spf.append(SPF(spf_name,spf_des,spf_types,spf_selector,spf_from_node,spf_to_node))
    if data["polUni"]["children"][22]["infraInfra"]["children"][x].get('infraNodeP') is not None:
        spf_name = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP']["attributes"]["name"]
        spf_des = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP']["attributes"]["descr"]
        spf_types = 'Leaf'
        if data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP'].get('children') is not None:
            if data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP']["children"][1].get('infraLeafS') is not None:
                spf_selector = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP']["children"][1]["infraLeafS"]["attributes"]["name"]
                if data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP']["children"][1]["infraLeafS"]["children"][1].get('infraNodeBlk') is not None:
                    spf_from_node = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP']["children"][1]["infraLeafS"]["children"][1]["infraNodeBlk"]["attributes"]["from_"]  
                    spf_to_node = data["polUni"]["children"][22]["infraInfra"]["children"][x]['infraNodeP']["children"][1]["infraLeafS"]["children"][1]["infraNodeBlk"]["attributes"]["to_"]  
        spf.append(SPF(spf_name,spf_des,spf_types,spf_selector,spf_from_node,spf_to_node))


for x in range(len(spf)):
    list_spf_name.append(spf[x].name)
    list_spf_des.append(spf[x].des)
    list_spf_types.append(spf[x].types)
    list_spf_selector.append(spf[x].selector)
    list_spf_from_node.append(spf[x].from_node)
    list_spf_to_node.append(spf[x].to_node)


#vPC Domain
#list vPC Domain
vpc = []
list_vpc_name = []
list_vpc_left_node = []
list_vpc_right_node = []
list_vpc_pair_id = []
#CLASS FOR vPC Domain
class vPC:
    def __init__(self,name,leaf_node,right_node,pair_id):   
        self.name = name
        self.leaf_node = leaf_node
        self.right_node = right_node
        self.pair_id = pair_id

for x in data["polUni"]["children"][23]["fabricInst"]["children"][78]["fabricProtPol"]["children"]:
    if x.get('fabricExplicitGEp') is not None:
        vpc_name = x["fabricExplicitGEp"]["attributes"]["name"]
        vpc_pair_id = x["fabricExplicitGEp"]["attributes"]["id"]

        if x["fabricExplicitGEp"]["children"][1].get('fabricNodePEp') is not None:
            vpc_left_node = x["fabricExplicitGEp"]["children"][1]["fabricNodePEp"]["attributes"]["id"]
        if x["fabricExplicitGEp"]["children"][2].get('fabricNodePEp') is not None:    
            vpc_right_node = x["fabricExplicitGEp"]["children"][2]["fabricNodePEp"]["attributes"]["id"]
        vpc.append(vPC(vpc_name,vpc_left_node,vpc_right_node,vpc_pair_id))
 
for x in range(len(vpc)):
    list_vpc_name.append(vpc[x].name)
    list_vpc_left_node.append(vpc[x].leaf_node)
    list_vpc_right_node.append(vpc[x].right_node)
    list_vpc_pair_id.append(vpc[x].pair_id)

#Bridge Domain
#list BD
bd = []
list_bd_name = []
list_bd_vrf = []
list_bd_des = []
list_bd_tenant = []
list_bd_gateway_ip =[]
list_bd_mac = []
list_bd_subnet_type = []
#CLASS FOR BD
class BD:
    def __init__(self,tn,vrf,name,des,mac,ip,subnet_type):   
        self.tn = tn
        self.vrf = vrf
        self.name = name
        self.des = des
        self.mac = mac
        self.ip = ip
        self.subnet_type = subnet_type


count = int(len(data["polUni"]["children"]))
      #BD
for x in range(count):
    bd_name = ''
    bd_des = ''
    bd_tenant = ''
    bd_mac = ''
    bd_gateway_ip = ''
    bd_vrf = ''
    bd_subnet_type = ''
    if data["polUni"]["children"][x].get('fvTenant') is not None:
        fvtenant_count = int(len(data["polUni"]["children"][x]["fvTenant"]["children"]))
        bd_tenant = data["polUni"]["children"][x]["fvTenant"]["attributes"]["name"]
        for y in range(fvtenant_count):
            if data["polUni"]["children"][x]["fvTenant"]["children"][y].get('fvBD') is not None:
                bd_name = data["polUni"]["children"][x]["fvTenant"]["children"][y]["fvBD"]["attributes"]["name"]
                bd_des = data["polUni"]["children"][x]["fvTenant"]["children"][y]["fvBD"]["attributes"]["descr"]
                bd_mac = data["polUni"]["children"][x]["fvTenant"]["children"][y]["fvBD"]["attributes"]["mac"]
                     
                if data["polUni"]["children"][x]["fvTenant"]["children"][y]["fvBD"]["children"][0].get('fvSubnet') is not None:
                    bd_gateway_ip = data["polUni"]["children"][x]["fvTenant"]["children"][y]["fvBD"]["children"][0]["fvSubnet"]["attributes"]["ip"]
                    bd_vrf = data["polUni"]["children"][x]["fvTenant"]["children"][y]["fvBD"]["children"][3]["fvRsCtx"]["attributes"]["tnFvCtxName"]
                    bd_subnet_type = data["polUni"]["children"][x]["fvTenant"]["children"][y]["fvBD"]["children"][0]["fvSubnet"]["attributes"]["scope"] 
                bd.append(BD(bd_tenant,bd_vrf,bd_name,bd_des,bd_mac,bd_gateway_ip,bd_subnet_type))  
        
for x in range(len(bd)):
    list_bd_name.append(bd[x].name)
    list_bd_vrf.append(bd[x].vrf)
    list_bd_des.append(bd[x].des)
    list_bd_tenant.append(bd[x].tn)
    list_bd_gateway_ip.append(bd[x].ip)
    list_bd_mac.append(bd[x].mac)
    list_bd_subnet_type.append(bd[x].subnet_type)


#Interface Policy Group
#list IPG
ipg = []
list_ipg_name = []
list_ipg_switch_type = []
list_ipg_interface_policy_group_type = []
list_ipg_aaep = []
list_ipg_link = []
list_ipg_cdp = []
list_ipg_lldp = []
list_ipg_stp = []
list_ipg_lacp = []
list_ipg_mcp = []

#CLASS FOR IPG
class IPG:
    def __init__(self,name,switch_type,ipg_group,aaep,link,cdp,lldp,stp,lacp,mcp):
        self.name = name
        self.switch_type = switch_type
        self.ipg_group = ipg_group
        self.aaep = aaep
        self.link = link
        self.cdp = cdp
        self.lldp = lldp
        self.stp = stp
        self.lacp = lacp
        self.mcp = mcp
        
count = int(len(data["polUni"]["children"][22]["infraInfra"]["children"][1233]["infraFuncP"]["children"]))

#infraAccBndlGrp = vPC
#infraAccPortGrp = Access
for x in range(count): 
    ipg_name = ''
    ipg_interface_policy_group_type = ''
    ipg_switch_type = ''
    ipg_aaep = ''
    ipg_link = ''
    ipg_cdp = ''
    ipg_lldp = ''
    ipg_stp = ''
    ipg_lacp = ''
    ipg_mcp = ''
    if data["polUni"]["children"][22]["infraInfra"]["children"][1233]["infraFuncP"]["children"][x].get('infraAccPortGrp') is not None:
        #IPG access 
        ipg_name = data["polUni"]["children"][22]["infraInfra"]["children"][1233]["infraFuncP"]["children"][x]["infraAccPortGrp"]["attributes"]["name"]  
        ipg_interface_policy_group_type = 'Access'
        ipg_switch_type = 'leaf'
        for y in data["polUni"]["children"][22]["infraInfra"]["children"][1233]["infraFuncP"]["children"][x]["infraAccPortGrp"]["children"]:
            if y.get('infraRsAttEntP') is not None:
                ipg_aaep = y["infraRsAttEntP"]["attributes"]["tDn"]
            if y.get('infraRsHIfPol') is not None:
                ipg_link =  y["infraRsHIfPol"]["attributes"]["tnFabricHIfPolName"]
            if y.get('infraRsCdpIfPol') is not None:
                ipg_cdp = y["infraRsCdpIfPol"]["attributes"]["tnCdpIfPolName"]
            if y.get('infraRsLldpIfPol') is not None:
                ipg_lldp = y["infraRsLldpIfPol"]["attributes"]["tnLldpIfPolName"]
            if y.get('infraRsStpIfPol') is not None:
                ipg_stp = y["infraRsStpIfPol"]["attributes"]["tnStpIfPolName"]
            if y.get('infraRsLacpPol') is not None:
                ipg_lacp = y["infraRsLacpPol"]["attributes"]["tnLacpLagPolName"]
            if y.get('infraRsMcpIfPol') is not None:
                ipg_mcp = y["infraRsMcpIfPol"]["attributes"]["tnMcpIfPolName"]
    if data["polUni"]["children"][22]["infraInfra"]["children"][1233]["infraFuncP"]["children"][x].get('infraAccBndlGrp') is not None:
        #IPG vPC
        ipg_name = data["polUni"]["children"][22]["infraInfra"]["children"][1233]["infraFuncP"]["children"][x]["infraAccBndlGrp"]["attributes"]["name"]
        ipg_interface_policy_group_type = 'vPC'
        ipg_switch_type = 'leaf'
        for y in data["polUni"]["children"][22]["infraInfra"]["children"][1233]["infraFuncP"]["children"][x]["infraAccBndlGrp"]["children"]:
            if y.get('infraRsAttEntP') is not None:
                ipg_aaep = y["infraRsAttEntP"]["attributes"]["tDn"]
            if y.get('infraRsHIfPol') is not None:
                ipg_link =  y["infraRsHIfPol"]["attributes"]["tnFabricHIfPolName"]
            if y.get('infraRsCdpIfPol') is not None:
                ipg_cdp = y["infraRsCdpIfPol"]["attributes"]["tnCdpIfPolName"]
            if y.get('infraRsLldpIfPol') is not None:
                ipg_lldp = y["infraRsLldpIfPol"]["attributes"]["tnLldpIfPolName"]
            if y.get('infraRsStpIfPol') is not None:
                ipg_stp = y["infraRsStpIfPol"]["attributes"]["tnStpIfPolName"]
            if y.get('infraRsLacpPol') is not None:
                ipg_lacp = y["infraRsLacpPol"]["attributes"]["tnLacpLagPolName"]
            if y.get('infraRsMcpIfPol') is not None:
                ipg_mcp = y["infraRsMcpIfPol"]["attributes"]["tnMcpIfPolName"]
    ipg.append(IPG(ipg_name,ipg_switch_type,ipg_interface_policy_group_type,ipg_aaep,ipg_link,ipg_cdp,ipg_lldp,ipg_stp,ipg_lacp,ipg_mcp))  
    

for x in range(len(ipg)):
    list_ipg_name.append(ipg[x].name)
    list_ipg_switch_type.append(ipg[x].switch_type)
    list_ipg_interface_policy_group_type.append(ipg[x].ipg_group)
    list_ipg_aaep.append(ipg[x].aaep)
    list_ipg_link.append(ipg[x].link)
    list_ipg_cdp.append(ipg[x].cdp)
    list_ipg_lldp.append(ipg[x].lldp)
    list_ipg_stp.append(ipg[x].stp)
    list_ipg_lacp.append(ipg[x].lacp)
    list_ipg_mcp.append(ipg[x].mcp)

now = datetime.now() 
# current date and time
date_time = now.strftime("%d-%m-%Y_%H-%M")
# Create some Pandas dataframes from some data.
sheet1 = pd.DataFrame({'ID': list_inventory_id,'role': list_inventory_role,'name': list_inventory_name,'pod': list_inventory_pod,'Serial Number': list_inventory_sn,'OOBv4':list_inventory_oobv4})
sheet2 = pd.DataFrame({'tenant': list_bd_tenant,'vrf': list_bd_vrf,'name': list_bd_name,'description': list_bd_des,'bd_mac': list_bd_mac,'bd_gateway_ip': list_bd_gateway_ip,'subnet_type':list_bd_subnet_type})
sheet3 = pd.DataFrame({'name': list_ipg_name,'switch_type': list_ipg_switch_type,'interface_policy_group_type': list_ipg_interface_policy_group_type,'aaep': list_ipg_aaep,'link_pol': list_ipg_link,'cdp_pol':list_ipg_cdp,'lldp_pol':list_ipg_lldp,'stp_pol':list_ipg_stp,'lacp_pol':list_ipg_lacp,'mcp_pol':list_ipg_mcp})
sheet4 = pd.DataFrame({'name': list_spf_name,'description': list_spf_des,'switch_profile_type': list_spf_types,'switch_selector': list_spf_selector,'from_node_id': list_spf_from_node,'to_node_id':list_spf_to_node})
sheet5 = pd.DataFrame({'name': list_vpc_name,'left_node_id': list_vpc_left_node,'right_node_id': list_vpc_right_node,'logical_pair_id': list_vpc_pair_id})
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(f"ACI Infomation {date_time}.xlsx", engine='xlsxwriter')
# Write each dataframe to a different worksheet.
sheet1.to_excel(writer, sheet_name='ACI Hostname')
sheet2.to_excel(writer, sheet_name='Bridge Domain')
sheet3.to_excel(writer, sheet_name='interface_policy_group')
sheet4.to_excel(writer, sheet_name='switch_profile')
sheet5.to_excel(writer, sheet_name='vpc_domain')
# Close the Pandas Excel writer and output the Excel file.
writer.save()    
