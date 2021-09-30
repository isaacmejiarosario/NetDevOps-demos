from genie.testbed import load
from pyats import aetest
from genie.utils import Dq
import json

class BgpTestcase(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)
        

    @aetest.test
    def bgp_state_af_ipv4(self):
          for device in self.parameters["testbed"].devices.values():
            os = device.os
            if os == "iosxr":
                bgp_status = device.parse('show bgp ipv4 unicast neighbors')
                bgp_vrfs = bgp_status.q.get_values('vrf')
                with open(f"/root/NETDEVOPS/NORNIR/PROJECTS/DEMOS/Test/golden_ops/{device.name}_show-bgp-ipv4-unicast-neighbors_parsed.txt", "rb") as file:
                    golden_template = json.load(file)
                    for vrf in bgp_vrfs:
                        current_vrf = bgp_status['instance']['all']['vrf'][vrf]
                        bgp_neighbors = Dq(current_vrf).get_values("neighbor")
                        golden_vrf = golden_template['instance']['all']['vrf'][vrf]
                        golden_bgp_neighbors = Dq(golden_vrf).get_values("neighbor")
                        for neighbor in golden_bgp_neighbors:
                            current_states = Dq(current_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
                            golden_states = Dq(golden_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
                            try:
                                assert neighbor in bgp_neighbors
                            except Exception as e:
                                self.failed(f"{device.name} {neighbor} is not active int vrf {vrf}")
              
    @aetest.test
    def bgp_state_af_vpnv4(self):
          for device in self.parameters["testbed"].devices.values():
            os = device.os
            if os == "iosxr":
                bgp_status = device.parse('show bgp ipv4 unicast neighbors')
                bgp_vrfs = bgp_status.q.get_values('vrf')
                with open(f"/root/NETDEVOPS/NORNIR/PROJECTS/DEMOS/Test/golden_ops/{device.name}_show-bgp-ipv4-unicast-neighbors_parsed.txt", "rb") as file:
                    golden_template = json.load(file)
                    for vrf in bgp_vrfs:
                        current_vrf = bgp_status['instance']['all']['vrf'][vrf]
                        bgp_neighbors = Dq(current_vrf).get_values("neighbor")
                        golden_vrf = golden_template['instance']['all']['vrf'][vrf]
                        golden_bgp_neighbors = Dq(golden_vrf).get_values("neighbor")
                        for neighbor in golden_bgp_neighbors:
                            current_states = Dq(current_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
                            golden_states = Dq(golden_vrf).contains_key_value("neighbor", neighbor).get_values("session_state")
                            try:
                                assert neighbor in bgp_neighbors
                            except Exception as e:
                                self.failed(f"{device.name} {neighbor} is not active int vrf {vrf}")

#class CommonCleanup(aetest.CommonCleanup):
#    @aetest.subsection
#    def disconnect_from_devices(self, testbed):
#        # disconnect_all
#        for device in self.parameters["testbed"].devices.values():
#            device.disconnect()
              
if __name__ == '__main__':
    topology = load('test-bed.yaml')
    aetest.main(testbed=topology)