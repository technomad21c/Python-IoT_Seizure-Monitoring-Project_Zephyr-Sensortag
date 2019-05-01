
from SensorPosition import *

class SensorInfo:
    def __init__(self, filename):
        self.fname = filename
        self.openFile()

    def openFile(self):
        with open(self.fname, "r") as f:
            leftArm = f.readline().rstrip('\n').split("=")[1].strip().split(',')
            leftArm_vendor = leftArm[1].lstrip().rstrip()
            leftArm_addr = leftArm[0].lstrip().rstrip()

            rightArm = f.readline().rstrip('\n').split("=")[1].strip().split(',')
            rightArm_vendor = rightArm[1].lstrip().rstrip()
            rightArm_addr = rightArm[0].lstrip().rstrip()

            leftAnkle = f.readline().rstrip('\n').split("=")[1].strip().split(',')
            leftAnkle_vendor = leftAnkle[1].lstrip().rstrip()
            leftAnkle_addr = leftAnkle[0].lstrip().rstrip()

            rightAnkle = f.readline().rstrip('\n').split("=")[1].strip().split(',')
            rightAnkle_vendor = rightAnkle[1].lstrip().rstrip()
            rightAnkle_addr = rightAnkle[0].lstrip().rstrip()

            self.sensorAddr = {LA: leftArm_addr, RA: rightArm_addr, LK: leftAnkle_addr,
                          RK: rightAnkle_addr}
            self.sensorVendor = {LA: leftArm_vendor, RA: rightArm_vendor, LK: leftAnkle_vendor,
                            RK: rightAnkle_vendor}

    def getSensorInfo(self, position):
        sensorinfo = {}
        if position == LA:
            sensorinfo = {"address": self.sensorAddr[LA], "vendor":self.sensorVendor[LA]}
        elif position == RA:
            sensorinfo = {"address": self.sensorAddr[RA], "vendor": self.sensorVendor[RA]}
        elif position == LK:
            sensorinfo = {"address": self.sensorAddr[LK], "vendor": self.sensorVendor[LK]}
        elif position == RK:
            sensorinfo = {"address": self.sensorAddr[RK], "vendor": self.sensorVendor[RK]}

        return sensorinfo
