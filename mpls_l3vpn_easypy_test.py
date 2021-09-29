import os
from pyats.easypy import run

####I.MEJIA_MPLS_L3VPN_NetDevOps_CI/CI_PIPELINE_LAB#####
def main(runtime):
    runtime.job.name = 'mpls_l3vpn_easypy_test'
    #script_path = f"{os.path.dirname(os.path.abspath(__file__))}/Test"
    script_path = os.path.dirname(os.path.abspath(__file__))
    ospf_test = os.path.join(script_path, 'ospf_test_all_vrfs.py')
    ldp_test = os.path.join(script_path, 'ldp_test.py')
    bgp_test = os.path.join(script_path, 'bgp_test_all_vrfs.py')
    ping_test = os.path.join(script_path, 'ping_test.py')
    run(testscript = ospf_test, runtime = runtime)
    run(testscript = ldp_test, runtime = runtime)
    run(testscript = bgp_test, runtime = runtime)
    run(testscript = ping_test, runtime = runtime)

""" access runtime information, such as runtime directory eg, save a new file into runtime directory"""