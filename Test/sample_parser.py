from genie.testbed import load
from pyats.async_ import pcall
from genie.utils import Dq
from rich import print
import json




#dev = tb.devices['CPE1']
#dev.connect(log_stdout=False)

def ospf_status(tb_value, dev):
    ospf_neighbor = tb_value.parse('show ip ospf database')
    pretty_print = json.dumps(ospf_neighbor, indent=2)
    #print (f"{dev }\n {pretty_print}\n\n")
    #ospf_state = ospf_neighbor.q.contains("state").get_values("state")
    #ospf_state = (Dq(ospf_neighbor).contains("state").get_values("state"))
    #ospf_routes = ospf_neighbor.q.contains_key_value("",1).get_values("lsa_id")
    ospf_state = ospf_neighbor.q.contains_key_value("lsa_types", 1).get_values("lsa_id")
    print(ospf_state)
    with open("golden_ops/golden-show-ip-ospf-database_parsed.txt") as f:
        #r = json.load(f)
        golden_ops = Dq(json.load(f)).contains_key_value("lsa_types", "1").get_values("lsa_id")
        print(golden_ops)

testbed = load('test-bed.yaml')
testbed.connect(log_stdout=False)
result = pcall(ospf_status, dev=testbed.devices.keys(), tb_value=testbed.devices.values())
