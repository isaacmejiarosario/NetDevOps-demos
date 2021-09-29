from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get, netconf_get_config, netconf_edit_config, netconf_commit
from nornir_pyez.plugins.tasks import *
from nornir_utils.plugins.functions import print_result, print_title
from nornir.core.filter import F 
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file="config.yaml", dry_run=False)

junos_group = nr.filter(F(groups__contains="junos_group"))
iosxr_group = nr.filter(F(groups__contains="iosxr_group"))

def load_vars(task):
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    mpls_config(task)
    
def mpls_config(task):
    if task.host.platform == "iosxr":
        vrf = task.run(task=template_file, template="vrf.j2", path=f"templates/{task.host.platform}/")
        task.run(task=netconf_edit_config, target="candidate", config=vrf.result)
        ospf = task.run(task=template_file, template="ospf.j2", path=f"templates/{task.host.platform}/")
        task.run(task=netconf_edit_config, target="candidate", config=ospf.result)
        bgp = task.run(task=template_file, template="bgp.j2", path=f"templates/{task.host.platform}/")
        task.run(task=netconf_edit_config, target="candidate", config=bgp.result)
        intf = task.run(task=template_file, template="intf.j2", path=f"templates/{task.host.platform}/")
        task.run(task=netconf_edit_config, target="candidate", config=intf.result)
        task.run(task=netconf_commit)     
    else:
        mpls = task.run(task=template_file, template="mpls-l3vpn.j2", path=f"templates/{task.host.platform}/")
        task.run(task=pyez_config, payload= mpls.result, data_format='xml')
        diff = task.run(task=pyez_diff)
        if diff:
            task.run(task=pyez_commit)
    
output = nr.run(task=load_vars)
print_result(output)