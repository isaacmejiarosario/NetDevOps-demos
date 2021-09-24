from genie.testbed import load
from pyats.async_ import pcall
from genie.utils import Dq
from rich import print
import json




#dev = tb.devices['CPE1']
#dev.connect(log_stdout=False)

def ospf_status(tb_value, dev):
    ospf_sessions = tb_value.parse('show ospf vrf all-inclusive neighbor detail')
    #pretty_print = json.dumps(ospf_neighbor, indent=2)
    #print (pretty_print)
    vrfs = ospf_sessions["vrf"]
    for vrf in vrfs:
        current_vrf = ospf_sessions["vrf"][vrf]
        #print(current_vrf)
        ospf_intfs = Dq(current_vrf).contains("interfaces").get_values("interfaces")
        print(ospf_intfs)
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
    #ospf_state = ospf_neighbor.q.contains("state").get_values("state")
    #ospf_state = (Dq(ospf_neighbor).contains("state").get_values("state"))
    #ospf_routes = ospf_neighbor.q.contains_key_value("",1).get_values("lsa_id")
   # ospf_state = ospf_neighbor.q.contains_key_value("lsa_types", 1).get_values("lsa_id")
   # print(ospf_state)
   # with open("golden_ops/golden-show-ip-ospf-database_parsed.txt") as f:
        #r = json.load(f)
    #    golden_ops = Dq(json.load(f)).contains_key_value("lsa_types", "1").get_values("lsa_id")
    #    print(golden_ops)

testbed = load('test-bed.yaml')
testbed.connect(log_stdout=False)
result = pcall(ospf_status, dev=testbed.devices.keys(), tb_value=testbed.devices.values())
