from nornir import InitNornir
import os
from nornir_utils.plugins.functions import print_result, print_title
from nornir_napalm.plugins.tasks import napalm_get, napalm_configure, napalm_cli
from nornir_scrapli.tasks import send_commands_from_file
from nornir.core.filter import F 
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml

script_dir = os.path.dirname(os.path.realpath(__file__))

nr = InitNornir(config_file=config.yaml, dry_run=False)

cisco_group = nr.filter(F(groups__contains="cisco_group"))
junos_group = nr.filter(F(groups__contains="junos_group"))

def load_vars(task):
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    basic_config(task)
    #output = data.result
    #send = output.splitlines()
#    import ipdb
#    ipdb.set_trace()

def basic_config(task):
    r = task.run(task=template_file, template="ntp.j2", path=f"templates/{task.host.platform}/")
    output = r.result
    task.run(task=napalm_configure, configuration= output)
  
      
def get_facts(task):
    task.run(task=napalm_get, getters= "get_arp_table")
    
def config(task):
    task.run(task=napalm_configure, filename= "ntp-config.txt")

def config_cli(task):
    task.run(task=napalm_cli, commands= ["show run | sec ntp"])
   
print_title("RUNBOOK TO CONFIGURE NTP")
result = nr.run(task=load_vars)
print_result(result)

#import ipdb
#ipdb.set_trace()

