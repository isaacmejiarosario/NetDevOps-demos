from genie.testbed import load
from pyats import aetest
from genie.utils import Dq
import json

class PingTestcase(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.parameters["testbed"].connect(log_stdout=False)
        self.device_list = ["172.20.100.1","172.20.100.2","172.20.100.21"]

        
    @aetest.test
    def ping_test(self):
        try:
            for device in self.parameters["testbed"].devices.values():
                for dest in self.device_list:
                    ping_result = device.parse(f"ping {dest} source loopback 0 repeat 3").q.contains("success_rate_percent").get_values("success_rate_percent")[0]
                    assert ping_result == 100.0
        except Exception as e:
            self.failed(f"{device.name} failed to reach loopback")


class CommonCleanup(aetest.CommonCleanup):
    def disconnect_from_devices(self):
        for device in self.parameters["testbed"].devices.values():
            device.disconnect()
              
if __name__ == '__main__':
    topology = load('test-bed.yaml')
    aetest.main(testbed=topology)


