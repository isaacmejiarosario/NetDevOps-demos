from genie.testbed import load
from pyats.async_ import pcall
from genie.utils import Dq
from rich import print
import json

device_list = ["172.20.100.1","172.20.100.2","172.20.100.21"]

#####################################################################
###                    REGULAR EXECUTION                          ###
##################################################################### 
tb = load('test-bed.yaml')
for device in tb.devices.values():
    device.connect(log_stdout=False)
    for dest in device_list:
        ping_result = device.parse(f"ping {dest} source loopback 0 repeat 3").q.contains("success_rate_percent").get_values("success_rate_percent")[0]
        print (ping_result)

#####################################################################
###                    PARALLEL EXECUTION                         ###
#####################################################################


#def ping_test(tb_value, dev):
#    try:
#        ping_loopbacks = tb_value.parse('ping 172.20.100.21 source loopback 0 repeat 3')
#        pretty_print = json.dumps(ping_loopbacks, indent=2)
#        print(pretty_print)
#    except Exception as e:
#        print(f"{dev} failed to reach loopback")

    #ping_result = ping_loopbacks.q.contains("success_rate_percent").get_values("success_rate_percent")
    #ping_result =  ping_loopbacks["ping"]["statistics"]['success_rate_percent']
    #if ping_result == 100.0:
        #print (f"{dev} is ok")
    #else:
        #print(f"{dev} is not ok")

#testbed = load('test-bed.yaml')
#testbed.connect(log_stdout=False)
#result = pcall(ping_test, dev=testbed.devices.keys(), tb_value=testbed.devices.values())
