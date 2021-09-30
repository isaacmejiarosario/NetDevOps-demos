from genie.testbed import load
from pyats import aetest
from pyats.async_ import pcall
from genie.utils import Dq
import json

class PingTestcase(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)
        self.ipv4_list_grt  = ["172.20.100.1","172.20.100.13","172.20.100.14","172.20.100.21","172.20.100.22"]

    @aetest.test
    def ping_test(self):
        for device in self.parameters["testbed"].devices.values():
            os = device.os
            if os == "iosxr":
                for dest in self.ipv4_list_grt:
                    ping_result = device.parse(f"ping {dest} source loopback0 repeat 4").q.get_values("success_rate_percent")[0]
                    try:
                        assert ping_result >= 75.0
                    except Exception as e:
                        self.failed(f"{device.name} failed to reach loopback with ipv4 address {dest}")
            elif os == "junos":
                for dest in self.ipv4_list_grt:
                    ping_result = device.parse(f"ping {dest} count 4 ").q.get_values('received')[0]
                    try:
                        assert ping_result >= 3
                    except Exception as e:
                        self.failed(f"{device.name} failed to reach loopback with ipv4 address {dest}")

class CommonCleanup(aetest.CommonCleanup):
    def disconnect_from_devices(self):
        for device in self.parameters["testbed"].devices.values():
            device.disconnect()
              
if __name__ == '__main__':
    topology = load('test-bed.yaml')
    aetest.main(testbed=topology)


