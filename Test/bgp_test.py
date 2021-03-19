from genie.testbed import load
from pyats import aetest
from genie.utils import Dq
import json

class BgpTestcase(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)
        with open(f"./golden_ops/golden-ospf-database.txt",  "rb") as f:
            self.routers =  Dq(json.load(f)).contains_key_value("lsa_types", "1").get_values("lsa_id")

    @aetest.test
    def bgp_status(self):
        for device in self.parameters["testbed"].devices.values():
            ospf_state = device.parse('show ip ospf neighbor').q.get_values("state")
            ospf_neighbors = device.parse('show ip ospf neighbor').q.get_values("neighbors")
            with open(f"./golden_ops/{device.name}_show-ip-ospf-neighbor_parsed.txt",  "rb") as f:
                neighbors = Dq(json.load(f)).get_values("neighbors")
                for neighbor in neighbors:
                    assert neighbor in ospf_neighbors
            for current_state in ospf_state:
                desired_state = "full"
                assert desired_state in current_state.lower()

    @aetest.test
    def ospf_database(self):
        #router_ids = ["172.20.100.1","172.20.100.2","172.20.100.21"]
        for device in self.parameters["testbed"].devices.values():
            ospf_topology = device.parse("show ip ospf database").q.contains_key_value("lsa_types", 1).get_values("lsa_id")
            for router in self.routers:
                assert router in ospf_topology

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        # disconnect_all
        for device in self.parameters["testbed"].devices.values():
            device.disconnect()
              
if __name__ == '__main__':
    topology = load('test-bed.yaml')
    aetest.main(testbed=topology)


