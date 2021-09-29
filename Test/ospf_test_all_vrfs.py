from genie.testbed import load
from pyats import aetest
from genie.utils import Dq
import json

class OspfTestcase(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)

    @aetest.test
    def ospf_status(self):
        for device in self.parameters["testbed"].devices.values():
            os = device.os
            if os == "iosxr":
                ospf_status = device.parse('show ospf vrf all-inclusive neighbor detail')
                ospf_vrfs = ospf_status.q.get_values('vrf')
                with open(f"./golden_ops/{device.name}_show-ospf-vrf-all-inclusive-neighbor-detail_parsed.txt", "rb") as file:
                    golden_template = json.load(file)
                    for vrf in ospf_vrfs:
                        current_vrf = ospf_status["vrf"][vrf]
                        ospf_intfs = Dq(current_vrf).contains("interfaces").get_values("interfaces")
                        golden_vrfs = golden_template["vrf"][vrf]
                        golden_intfs = Dq(golden_vrfs).contains("interfaces").get_values("interfaces")
                        for int in golden_intfs:
                            golden_neighbors = Dq(golden_vrfs).contains_key_value("interfaces", int).get_values("neighbors")
                            golden_states = Dq(golden_vrfs).contains_key_value("interfaces", int).get_values("state")
                            current_neighbors = Dq(current_vrf).contains_key_value("interfaces", int).get_values("neighbors")
                            current_states = Dq(current_vrf).contains_key_value("interfaces", int).get_values("state")
                            try:
                                assert int in ospf_intfs
                            except Exception as e:
                                self.failed(f"{device.name} {int} is not active int vrf {vrf}")
                            try:
                                assert golden_neighbors == current_neighbors
                            except Exception as e:
                                self.failed(f"{device.name} {golden_neighbors} over Interface {int} Is not active")
                            try:
                                assert golden_states == current_states
                            except Exception as e:
                                self.failed(f"{device.name} {golden_neighbors} over Interface {int} Is {current_states}")
            elif os == "junos":
                ospf_status = device.parse('show ospf neighbor instance all')
                ospf_sessions = ospf_status.q.get_values('ospf-neighbor')
                with open(f"./golden_ops/{device.name}_show-ospf-neighbor-instance-all_parsed.txt", "rb") as file:
                    golden_template = json.load(file)
                    golden_sessions =  Dq(golden_template).get_values("ospf-neighbor")
                    for session in golden_sessions:
                        ospf_vrfs = ospf_status.q.get_values("ospf-instance-name")
                        ospf_intfs = Dq(ospf_sessions[0]).get_values('interface-name')
                        golden_vrfs = Dq(golden_template).get_values('ospf-instance-name')
                        golden_intfs = Dq(golden_template).get_values('interface-name')
                        for int in golden_intfs:
                            golden_neighbors = Dq(session).get_values("neighbor-id")
                            golden_states = Dq(session).get_values('ospf-neighbor-state')
                            current_neighbors = Dq(ospf_sessions[0]).get_values("neighbor-id")
                            current_states = Dq(ospf_sessions[0]).get_values("ospf-neighbor-state")
                            try:
                                assert int in ospf_intfs
                            except Exception as e:
                                self.failed(f"{device.name} {int} is not active")
                            try:
                                assert golden_neighbors == current_neighbors
                            except Exception as e:
                                self.failed(f"{device.name} {golden_neighbors} over Interface {int} Is not active")
                            try:
                                assert golden_states == current_states
                            except Exception as e:
                                self.failed(f"{device.name} {golden_neighbors} over Interface {int} Is {current_states}")


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        # disconnect_all
        for device in self.parameters["testbed"].devices.values():
            device.disconnect()
              
if __name__ == '__main__':
    topology = load('test-bed.yaml')
    #topology = tb.devices['TH-RTR01-9910']
    aetest.main(testbed=topology)