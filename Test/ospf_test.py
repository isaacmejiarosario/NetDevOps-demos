from genie.testbed import load
from pyats import aetest
from genie.utils import Dq
import json

class OspfTestcase(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)
        with open(f"./golden_ops/golden-ospf-database.txt",  "rb") as f:
            self.routers =  Dq(json.load(f)).contains_key_value("lsa_types", "1").get_values("lsa_id")

    @aetest.test
    def ospf_status(self):
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
    
    @aetest.test
    def ospf_routes(self):
        must_be_rt = ["11.11.11.11/32","172.20.100.1/32","172.20.100.2/32","172.20.100.21/32"]
        for device in self.parameters["testbed"].devices.values():
            get_routes = device.parse("show ip route").q.contains("ospf|connected", regex=True).get_values("routes")
            for route in must_be_rt:
                assert route in get_routes

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        # disconnect_all
        for device in self.parameters["testbed"].devices.values():
            device.disconnect()
              
if __name__ == '__main__':
    topology = load('test-bed.yaml')
    aetest.main(testbed=topology)


