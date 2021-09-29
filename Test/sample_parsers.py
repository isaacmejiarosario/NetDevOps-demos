from os import curdir
from genie.testbed import load
from pyats.async_ import pcall
from genie.utils import Dq
from genie.utils import *
from rich import print
import json




#dev = tb.devices['CPE1']
#dev.connect(log_stdout=False)

#def ospf_status(tb_value, dev):

###JUNOS SAMPLE PARSERS FOR OSPF######
######################################

def ospf_status_junos(dev):
    ospf_status = dev.parse('show ospf neighbor instance all')
    ospf_sessions =  ospf_status.q.contains_key_value("interface-name", "ge-0/0/0.0").get_values("ospf-neighbor")
    with open(f"./golden_ops/{dev.name}_show-ospf-neighbor-instance-all_parsed.txt", "rb") as file:
         golden_template = json.load(file)
         golden_sessions =  Dq(golden_template).contains("master").get_values("ospf-neighbor")
         #print (golden_template)
         print (golden_sessions)


    #print (ospf_status)
    #print (ospf_sessions)
    #ospf_sessions =  ospf_status["ospf-neighbor-information-all"]["ospf-instance-neighbor"]["ospf-neighbor"]
    ospf_vrfs = ospf_status.q.get_values("ospf-instance-name")
    intfs = Dq(ospf_status).contains("interface-name").get_values("interface-name")
    #vrf = ospf_status["ospf-neighbor-information-all"]["ospf-instance-neighbor"]['ospf-instance-name']
    #current_vrf = Dq(ospf_vrfs).contains_key_value("ospf-instance-name", vrf).get_values("ospf-neighbor")
    #for session in ospf_sessions:
        #ospf_intfs = Dq(session).get_values('interface-name')
        #with open(f"./golden_ops/{dev.name}_show-ospf-neighbor-instance-all_parsed.txt", "rb") as file:
        #with open(f"./golden_ops/{dev.name}_show-ospf-neighbor-detail_parsed.txt", "rb") as file:
           # golden_template = json.load(file)
           # golden_intfs = Dq(golden_template).get_values('interface-name')
            #golden_vrfs = Dq(golden_template).get_values('ospf-instance-name')
           # golden_sessions =  Dq(golden_template).get_values("ospf-neighbor")
    #for session in ospf_sessions:
     #   print (session)
      
    #pretty_print = json.dumps(ospf_neighbor, indent=2)
   
###IOSXR SAMPLE PARSERS FOR OSPF######
######################################
def ospf_status_iosxr(dev):
    ospf_status = dev.parse('show ospf vrf all-inclusive neighbor detail')
    ospf_vrfs = ospf_status["vrf"]
    for vrf in ospf_vrfs:
        current_vrf = ospf_status["vrf"][vrf]
        print (current_vrf)

        #with open(f"./golden_ops/{tb_value.name}_show-ospf-vrf-all-inclusive-neighbor-detail_parsed.txt", "rb") as file:
        #    golden_template = json.load(file)
        #    golden_vrfs = golden_template["vrf"][vrf]
        #    golden_intfs = Dq(golden_vrfs).contains("interfaces").get_values("interfaces")
        #    print (golden_intfs)
        #for int in ospf_intfs:
        #    current_session = Dq(vrfs).contains_key_value("interfaces", int).get_values("neighbors")
        #    current_state = Dq(vrfs).contains_key_value("interfaces", int).get_values("state")
        #    print(f"{current_session} is {current_state}")
    
    
    
    #print (f"{dev }\n {pretty_print}\n\n")
    
###IOSXR SAMPLE PARSERS FOR BGP######
######################################

def bgp_status_iosxr(dev):
    bgp_status = dev.parse('show bgp vpnv4 unicast neighbors')
    bgp_vrfs = bgp_status.q.get_values('vrf')
    with open(f"./golden_ops/{dev.name}_show-bgp-ipv4-unicast-neighbors_parsed.txt", "rb") as file:
        golden_template = json.load(file)
        for vrf in bgp_vrfs:
            current_vrf = bgp_status['instance']['all']['vrf'][vrf]
            bgp_neighbors = Dq(current_vrf).get_values("neighbor")
            golden_vrf = golden_template['instance']['all']['vrf'][vrf]
            golden_bgp_neighbors = Dq(golden_vrf).get_values("neighbor")
            for neighbor in golden_bgp_neighbors:
                current_states = Dq(current_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
                golden_states = Dq(golden_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
                print (current_states)
                print (golden_states)

###JUNOS SAMPLE PARSERS FOR BGP######
######################################

def bgp_status_junos(dev):
    bgp_status = dev.parse('show version')
    print (bgp_status)
    # bgp_vrfs = bgp_status.q.get_values('vrf')
    # with open(f"./golden_ops/{dev.name}_show-bgp-ipv4-unicast-neighbors_parsed.txt", "rb") as file:
    #     golden_template = json.load(file)
    #     for vrf in bgp_vrfs:
    #         current_vrf = bgp_status['instance']['all']['vrf'][vrf]
    #         bgp_neighbors = Dq(current_vrf).get_values("neighbor")
    #         golden_vrf = golden_template['instance']['all']['vrf'][vrf]
    #         golden_bgp_neighbors = Dq(golden_vrf).get_values("neighbor")
    #         for neighbor in golden_bgp_neighbors:
    #             current_states = Dq(current_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
    #             golden_states = Dq(golden_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
    #             print (current_states)
    #             print (golden_states)

###IOSXR SAMPLE PARSERS FOR MPLS######
######################################

def mpls_status_iosxr(dev):
    mpls_template = dev.parse('show mpls ldp  neighbor')
    mpls_status = mpls_template['vrf']['default']
    mpls_peers = Dq(mpls_template).get_values("peers")
    with open(f"golden_ops/{dev.name}_show-mpls-ldp-neighbor_parsed.txt", "rb") as f:
        golden_template = json.load(f)
        golden_peers = Dq(golden_template).get_values("peers")
        mpls_golden_status = golden_template['vrf']['default']
        for peer in golden_peers:
            current_state = Dq(mpls_status).contains_key_value("peers", peer).get_values("state")
            golden_state = Dq(mpls_golden_status).contains_key_value("peers", peer).get_values("state")
            print (current_state)
            print (golden_state)

###JUNOS SAMPLE PARSERS FOR MPLS######
######################################

def mpls_status_junos(dev):
    mpls_template = dev.parse('show ldp session')
    ldp_status = mpls_template['ldp-session-information']['ldp-session'][0]
    ldp_peers = Dq(ldp_status).get_values('ldp-neighbor-address')
    with open(f"golden_ops/{dev.name}_show-ldp-session_parsed.txt", "rb") as f:
        golden_template = json.load(f)
        ldp_golden_status = golden_template['ldp-session-information']['ldp-session']
        golden_peers = Dq(golden_template).get_values('ldp-neighbor-address')
        for session in ldp_golden_status:
            for peer in golden_peers:
                golden_state = Dq(session).get_values('ldp-session-state')
                current_state = Dq(mpls_template).contains(peer).get_values('ldp-session-state')
                print (peer)
                print (current_state)
                print (golden_state)

    # mpls_status = mpls_template['vrf']['default']
    # mpls_peers = Dq(mpls_template).get_values("peers")
    # with open(f"golden_ops/{dev.name}_show-mpls-ldp-neighbor_parsed.txt", "rb") as f:
    #     golden_template = json.load(f)
    #     golden_peers = Dq(golden_template).get_values("peers")
    #     mpls_golden_status = golden_template['vrf']['default']
    #     for peer in golden_peers:
    #         current_state = Dq(mpls_status).contains_key_value("peers", peer).get_values("state")
    #         golden_state = Dq(mpls_golden_status).contains_key_value("peers", peer).get_values("state")
    #         print (current_state)
    #         print (golden_state)
###IOSXR SAMPLE PARSERS FOR PING######
######################################
def ping_iosxr(dev):  
    ipv4_list_grt  = ["172.20.100.1","172.20.100.13","172.20.100.14","172.20.100.21","172.20.100.22"]
    for dest in ipv4_list_grt:
        ping_result = dev.parse(f"ping {dest} source loopback0 repeat 4").q.get_values("success_rate_percent")[0]
        result = ping_result >= 75.0     
        print(result)

###JUNOS SAMPLE PARSERS FOR PING######
######################################
def ping_junos(dev):  
    ipv4_list_grt  = ["172.20.100.1","172.20.100.13","172.20.100.14","172.20.100.21","172.20.100.22"]
    for dest in ipv4_list_grt:
        ping_result = dev.parse(f"ping {dest} count 4 ").q.get_values('received')[0]
        result = ping_result >= 3     
        print(result)

if __name__ == '__main__':
    testbed = load('test-bed.yaml')
    #topology = testbed.devices.values()
    dev = testbed.devices["IOS-XR-PE1"]
    dev_junos = testbed.devices["JPE3"]
    host = dev.name
    host2 = dev_junos.name
    #print (f"{host}")
    #dev.connect(log_stdout=False)
    #ping_junos(dev=dev)
    print (f"{host2}")
    dev_junos.connect(log_stdout=False)
    bgp_status_junos(dev=dev_junos)

###SAMPLE CODE TO EXECUTE PARALLEL CALLS TO ALL DEVICES IN THE TOPOLOGY####
#testbed.connect(log_stdout=False)
#result = pcall(ospf_status, dev=testbed.devices.keys(), tb_value=testbed.devices.values())
