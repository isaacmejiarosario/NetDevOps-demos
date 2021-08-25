from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get, netconf_get_config, netconf_edit_config, netconf_commit
from nornir_utils.plugins.functions import print_result, print_title
from xml.dom import minidom
from nornir.core.filter import F 
from nornir_jinja2.plugins.tasks import template_file
from rich import print
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_utils.plugins.tasks.files import write_file
from datetime import date
import pathlib

nr = InitNornir(config_file="config.yaml", dry_run=False)

devnet_group = nr.filter(F(groups__contains="devnet_group"))
cisco_group = nr.filter(F(groups__contains="cisco_group"))
iosxr_group = nr.filter(F(groups__contains="iosxr_group"))


def load_vars(task):
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    mpls_config(task)
   
def getter(task):
    result = task.run(task=netconf_get_config, source="running")
    result_pretty = minidom.parseString(result).toprettyxml()
    print (result_pretty)

def get_config_file(task):
    config_dir = "output"
    date_dir = config_dir + "/" + str(date.today())
    pathlib.Path(config_dir).mkdir(exist_ok=True)
    pathlib.Path(date_dir).mkdir(exist_ok=True)
    r = task.run(task=netconf_get, filter_="/native/vrf", filter_type="xpath")
    task.run(task=write_file, content=r.result, filename=str(date_dir) + f"/{task.host}.txt")

def basic_config(task):
    r = task.run(task=template_file, template="intf.j2", path=f"templates/{task.host.platform}/")
    output = r.result
    task.run(task=netconf_edit_config, target="candidate", config=output)
    task.run(task=netconf_commit)

def mpls_config(task):
    vrf = task.run(task=template_file, template="vrf.j2", path=f"templates/{task.host.platform}/")
    task.run(task=netconf_edit_config, target="candidate", config=vrf.result)
    ospf = task.run(task=template_file, template="ospf.j2", path=f"templates/{task.host.platform}/")
    task.run(task=netconf_edit_config, target="candidate", config=ospf.result)
    bgp = task.run(task=template_file, template="bgp.j2", path=f"templates/{task.host.platform}/")
    task.run(task=netconf_edit_config, target="candidate", config=bgp.result)
    intf = task.run(task=template_file, template="intf.j2", path=f"templates/{task.host.platform}/")
    task.run(task=netconf_edit_config, target="candidate", config=intf.result)
    task.run(task=netconf_commit)






output = iosxr_group.run(task=getter)
print_result(output)