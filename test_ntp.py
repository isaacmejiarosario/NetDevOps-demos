import pytest
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result, print_title
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.filter import F
from rich import print

nr = InitNornir(config_file="config.yaml")

cisco_group = nr.filter(F(groups__contains="cisco_group"))
junos_group = nr.filter(F(groups__contains="junos_group"))
devnet_group = nr.filter(F(groups__contains="devnet_group"))
eveng_lab = nr.filter(F(groups__contains="cisco_group") | F(groups__contains="junos_group"))

def ntp_stats(task):
    output = task.run(task=napalm_get,getters=["ntp_stats"]).result
    return output["ntp_stats"]
    
        
        
def test_ntp():
    r = cisco_group.run(task=ntp_stats)
    #print (r)
    for n in r:
        out = r[n].result
        syn = out[0]["synchronized"]
        assert syn == False
        print (syn)


test_ntp()