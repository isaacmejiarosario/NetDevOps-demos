from genie.testbed import load
from genie.utils.diff import Diff
from rich import print
import json


tb = load('test-bed.yaml')
learnt = {}
for name, dev in tb.devices.items():
    dev.connect(log_stdout=False)
    learnt[name] = {}
    learnt[name]['config'] = dev.learn('config')
    #ntp = learnt[name]['ntp']
    config = learnt[name]
    print (dict(config))
    print (type(dict(config)))
    #with open(f"./golden_ops/{name}_ntp.txt",  "rb") as f:
            #d = Diff()
        #d.findDiff()





    
    #print(type(current_conf))
    #with open(f"./current_ops/{name}_ntp-ops.txt", "wb") as f:
    #    f.write(current_conf)
    #with open(f"./current_ops/{name}_ntp-ops.txt",  "rb") as current:
    #    current_conf = json.load(current)
        #print(type(current_conf))
    #with open(f"./golden_ops/{name}_ntp.txt",  "rb") as golden:
    #    golden_conf = json.load(golden)
        #print(type(golden_conf))
    #    diff = Diff(golden_conf, current_conf)
    #    diff.findDiff()
    #    print(diff)
        #print(type(golden_conf))

    #dev = tb.devices['CPE1']
    #dev.connect(log_stdout=False)
    #result = dev.learn("ospf")
    #print (result.info)