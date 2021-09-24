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
            ospf_status = device.parse('show ospf vrf all-inclusive neighbor detail')
            ospf_vrfs = ospf_status["vrf"]
            for vrf in ospf_vrfs:
                current_vrf = ospf_status["vrf"][vrf]
                ospf_intfs = Dq(current_vrf).contains("interfaces").get_values("interfaces")
                with open(f"./golden_ops/{device.name}_show-ospf-vrf-all-inclusive-neighbor-detail_parsed.txt", "rb") as file:
                    golden_template = json.load(file)
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