import binascii
from bluepy import btle
import struct
import math
import time
from decimal import Decimal

SHOW_ACC_DATA = False


class BleSensor(object):
    ### Sensor Flag


    ### UUID for SensorTag CC2650
    acclUUID_sensortag = "f000aa80-0451-4000-b000-000000000000"  # Accelerometer Service UUID
    dataUUID_sensortag = "f000aa81-0451-4000-b000-000000000000"  # Characteristics for Accelerometer Data
    ctrlUUID_sensortag = "f000aa82-0451-4000-b000-000000000000"  # Characteristics for Accelerometer Control
    rateUUID_sensortag = "f000aa83-0451-4000-b000-000000000000"  # period (sampling rate)
    readData_sensortag = "<hhhhhhhhh"
    cmdEnable = "0x007f"
    cmdDisable = "0x0000"
    cmdPeriod = "0x01"

    def __init__(self, vendor, addr):
        self.addr = addr
        self.vendor = vendor

        if (vendor == "neblina"):
            self.acclUUID = self.acclUUID_neblina
            self.dataUUID = self.dataUUID_neblina
            self.ctrlUUID = self.ctrlUUID_neblina
            self.readData = self.readData_neblina
            self.cmdEnable = "0x01"
            self.cmdDisable = "0x00"

        elif (vendor == "sensortag"):
            self.acclUUID = self.acclUUID_sensortag
            self.dataUUID = self.dataUUID_sensortag
            self.ctrlUUID = self.ctrlUUID_sensortag
            self.rateUUID = self.rateUUID_sensortag
            self.readData = self.readData_sensortag
            self.cmdEnable = "0x00ff"
            self.cmdDisable = "0x00ff"
            self.cmdPeriod = "0x0a"

    def connect(self):
        print("connecting to a ", self.vendor, " device: ", self.addr)

        try:
            if (self.vendor == "neblina"):
                self.dev = btle.Peripheral(self.addr, "random")
            elif (self.vendor == "sensortag"):
                self.dev = btle.Peripheral(self.addr, "public")
        except Exception as err:
            print("[ERROR] Connection Error occurred! ")
            print(str(err))
            return False
        else:
            print("Successfully connected to a ", self.vendor, " device: ", self.addr)

        try:
            self.acclServ = self.dev.getServiceByUUID(self.acclUUID)
            print(self.acclServ)
            self.acclData = self.acclServ.getCharacteristics(self.dataUUID)[0]
            print(self.acclData)
            self.acclCtrl = self.acclServ.getCharacteristics(self.ctrlUUID)[0]
            print(self.acclCtrl)

            # enable sensortag
            if (self.vendor == "sensortag"):
                self.acclRate = self.acclServ.getCharacteristics(self.rateUUID)[0]
                self.acclCtrl.write(struct.pack("<H", 0x007f))
                self.acclRate.write(struct.pack("<B", int(self.cmdPeriod, 16)))
                print("successfully set to 100ms for sampling rate")

        except Exception as err:
            print("Accelerometer Service does not exist!")
            print(str(err))
            self.disconnect()
            return False
        else:
            print("Successfully received accelerometer service from a ", self.vendor, " sensor")
            return True

    def disconnect(self):
        self.dev.disconnect()

    def enable(self):
        if (self.vendor == "neblina"):
            self.acclCtrl.write(struct.pack("<B", 0x01))
        elif (self.vendor == "sensortag"):
            self.acclCtrl.write(struct.pack("<h", 0x00ff))
            # self.acclCtrl.write(struct.pack("<h", int(self.cmdEnable, 16)))

    def disable(self):
        if (self.vendor == "neblina"):
            self.acclCtrl.write(struct.pack("B", 0x00))
        elif (self.vendor == "sensortag"):
            self.acclCtrl.write(struct.pack("<h", int(self.cmdDisable, 16)))

    def read(self):
        timestamp = 0
        accl = [0] * 3
        gyro = [0] * 3
        magn = [0] * 3

        data = self.acclData.read()
        if (self.vendor == "neblina"):
            if SHOW_ACC_DATA:
                print("DATA: ", data, "SIZE: ", len(data))
            if len(data) == 14:
                header, timestamp, accl[0], accl[1], accl[2] = struct.unpack(self.readData,
                                                                             data)  # self.acclData.read())

        elif (self.vendor == "sensortag"):
            if SHOW_ACC_DATA:
                print("DATA: ", data, "SIZE: ", len(data))
            gyro[0], gyro[1], gyro[2], accl[0], accl[1], accl[2], magn[0], magn[1], magn[2] = struct.unpack(
                self.readData, data)

        accl[0] = round((accl[0] * 1.0) / (32768 / 8), 2)  # 4G
        accl[1] = round((accl[1] * 1.0) / (32768 / 8), 2)
        accl[2] = round((accl[2] * 1.0) / (32768 / 8), 2)
        
        gyro[0] = round((gyro[0] * 1.0) / (65536 / 500), 2)
        gyro[1] = round((gyro[1] * 1.0) / (65536 / 500), 2)
        gyro[2] = round((gyro[2] * 1.0) / (65536 / 500), 2)

        print(accl, gyro, magn)

        if SHOW_ACC_DATA:
            curtime = time.strftime("%Y%m%d, %H%M%S")
            print("    Time: %s Acceleration     :  [%4.2f, %4.2f, %4.2f]  %7s" % (curtime, accl[0], accl[1], accl[2], self.vendor))

        return accl, gyro, magn


if (__name__ == "__main__"):
    # sensortag
    vendor = "sensortag"
    addr_LA = "54:6c:0e:53:3e:e6"

    b = BleSensor(vendor, addr_LA)
    b.connect()

    while True:
        print(b.read())




