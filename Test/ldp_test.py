from genie.testbed import load
from pyats import aetest
from genie.utils import Dq
import json

class ldpTestcase(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)

    @aetest.test
    def mpls_ldp_status(self):
        for device in self.parameters["testbed"].devices.values():
            os = device.os
            if os == "iosxr":
                ldp_template = device.parse('show mpls ldp  neighbor')
                ldp_status = ldp_template['vrf']['default']
                ldp_peers = Dq(ldp_template).get_values("peers")
                with open(f"/root/NETDEVOPS/NORNIR/PROJECTS/DEMOS/Test/golden_ops/{device.name}_show-mpls-ldp-neighbor_parsed.txt", "rb") as f:
                    golden_template = json.load(f)
                    ldp_golden_status = golden_template['vrf']['default']
                    golden_peers = Dq(golden_template).get_values("peers")
                    for peer in golden_peers:
                        current_state = Dq(ldp_status).contains_key_value("peers", peer).get_values("state")
                        golden_state = Dq(ldp_golden_status).contains_key_value("peers", peer).get_values("state")
                        try:
                            assert peer in ldp_peers
                        except Exception as e:
                            self.failed(f"{peer} is NOT active ")
                        try:
                            assert golden_state == current_state
                        except Exception as e:
                            self.failed(f"{peer} failed is in {current_state} state ")
            elif os == "junos":
                ldp_template = device.parse('show ldp session')
                ldp_status = ldp_template['ldp-session-information']['ldp-session'][0]
                ldp_peers = Dq(ldp_status).get_values('ldp-neighbor-address')
                with open(f"/root/NETDEVOPS/NORNIR/PROJECTS/DEMOS/Test/golden_ops/{device.name}_show-ldp-session_parsed.txt", "rb") as f:
                    golden_template = json.load(f)
                    ldp_golden_status = golden_template['ldp-session-information']['ldp-session']
                    golden_peers = Dq(golden_template).get_values('ldp-neighbor-address')
                    for session in ldp_golden_status:
                        for peer in golden_peers:
                            golden_state = Dq(session).get_values('ldp-session-state')
                            current_state = Dq(ldp_status).get_values('ldp-session-state')
                            try:
                                assert peer in ldp_peers
                            except Exception as e:
                                self.failed(f"{peer} is NOT active ")
                            try:
                                assert golden_state == current_state
                            except Exception as e:
                                self.failed(f"{peer} failed is in {current_state} state ")


                        
                        
                
class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        # disconnect_all
        for device in self.parameters["testbed"].devices.values():
            device.disconnect()
              
if __name__ == '__main__':
    topology = load('test-bed.yaml')
    aetest.main(testbed=topology)

