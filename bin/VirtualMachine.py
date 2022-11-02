import argparse
import os
import time

# pip install google-api-python-client
import googleapiclient.discovery
from six.moves import input

compute = googleapiclient.discovery.build('compute', 'v1')


# [START list_instances]
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None
# [END list_instances]

class VirtualMachine:
    def __init__(self, computeService, config : str):
        self.name = config["name"]
        #startup_script = open(os.path.join(config["startup_script"], 'r').read()
        self.project = config["project"]
        self.zone = config["zone"]
        self.createConfig = {
            'name': self.name,
            'machineType': config["machine"],
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                    'sourceImage': config["os_image"]#"projects/debian-cloud/global/images/debian-11-bullseye-v20220920",
                    }   
                },
                {
                    'boot': False,
                    'autoDelete': True,
                    'initializeParams': {
                        'sizeGb': config["disk_size"]

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
            }]#,

       # 'metadata': {
       #      'items': [{
       #          'key': 'startup-script',
       #          'value': startup_script
       #      }]
       # }
        }

    def create(self):
        return self.compute.instances().insert(
        project=self.project,
        zone=self.zone,
        body=self.createConfig).execute()

    def delete(self):
        return self.compute.instances().delete(project = self.project ,zone = self.zone ,instance = self.name).execute()
