import sys, os
import googleapiclient.discovery
sys.path.insert(1, os.path.join(os.environ.get("HOME"), "cloudLab/bin"))
from settings import config
from VirtualMachine import VirtualMachine
from time import sleep

if __name__ == "__main__":

    gcloudCompute = googleapiclient.discovery.build('compute', 'v1')
    vm = VirtualMachine(gcloudCompute, "test", config)
    print(len(vm.listInstances()))
    vm.create()
    sleep(5)
    print(len(vm.listInstances()))
    sleep(20)
    vm.delete()
    sleep(20)
    print(len(vm.listInstances()))
