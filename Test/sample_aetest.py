# Example
# -------
#
#   very simple aetest testscript

from pyats import aetest
from some_lib import configure_interface

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_device(self, testbed):
        # connect to testbed devices
        for device in testbed:
            device.connect()

class SimpleTestcase(aetest.Testcase):
    @aetest.test
    def simple_test(self, testbed):
        # configure each device interface
        for device in testbed:
            for intf in device:
                configure_interface(intf)

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        # disconnect_all
        for device in testbed:
            device.disconnect()

# for running as its own executable
if __name__ == '__main__':
    aetest.main()