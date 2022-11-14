class Disk:
    def __init__(self, gcloudCompute, config, name : str = None, sizeGb : str= None):
        if name != None:
            self.name = name
        else:
            self.name = config["disk"]["name"]

        if sizeGb != None:
            self.sizeGb = sizeGb
        else:
            self.sizeGb = config["disk"]["sizeGb"]

        self.project = config["general"]["project"]
        self.zone = config["general"]["zone"]
        self.compute = gcloudCompute
        self.createConfig = {
                       "kind": string,
                       "name": self.name,
                       "sizeGb": self.sizeGb,
                       "zone": self.zone,
                       "sourceSnapshot": string,
                       "sourceSnapshotId": string,
                       "sourceStorageObject": string,
                       "sourceImage": string,
                       "sourceImageId": string,
                       "type": config["disk"]["type"]
                }
    def create(self):
        return self.compute.disks().insert(
        project=self.project,
        zone=self.zone,
        body=self.createConfig).execute()

    def delete(self):
        return self.compute.disks().delete(project = self.project ,zone = self.zone ,instance = self.name).execute()
