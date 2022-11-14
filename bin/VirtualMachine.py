import argparse
import os
import time
import googleapiclient.discovery
from six.moves import input


class VirtualMachine:

    def __init__(self, computeService, name, vmConfig):

        self.name = name
        self.compute = computeService
        self.project = vmConfig["general"]["project"]
        self.zone = vmConfig["general"]["zone"]
        if vmConfig["vm"].get("startupConfig", False):
            self.startup_script = open(os.path.join(vmConfig["vm"]["startup_script"], 'r')).read()
        else:
            self.startup_script = False
        self.project = vmConfig["general"]["project"]
        self.zone = vmConfig["general"]["zone"]
        self.createConfig = {
            'name': self.name,
            'machineType': vmConfig["vm"]["machine"],
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                    'sourceImage': vmConfig["vm"]["os_image"]
                    } 
                }
            ],

            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/devstorage.read_write',
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }]
        }
        if self.startup_script:
             self.createConfig["metadata"] = {'items': [{'key': 'startup-script','value': self.startup_script}]}
        
    def listInstances(self):
        result = self.compute.instances().list(project=self.project, zone=self.zone).execute()
        return result['items'] if 'items' in result else None

    def create(self):
        return self.compute.instances().insert(
        project=self.project,
        zone=self.zone,
        body=self.createConfig).execute()

    def delete(self):
        return self.compute.instances().delete(project = self.project ,zone = self.zone ,instance = self.name).execute()
