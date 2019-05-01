import binascii
from bluepy import btle
import struct
import math
import time
from decimal import Decimal

from SensorPosition import *

SHOW_ACC_DATA = False


class AccSensor(object):
    ### UUID for Neblina
    acclUUID_neblina = "0df9f021-1532-11e5-8960-0002a5d5c51b"  # Service for Accelerometer Sensor
    dataUUID_neblina = "0df9f022-1532-11e5-8960-0002a5d5c51b"  # Characteristics for Accelerometer Data
    ctrlUUID_neblina = "0df9f023-1532-11e5-8960-0002a5d5c51b"  # Characteristics for Accelerometer Control
    readData_neblina = "<llhhh"
    # readData_neblina = "<llhhhh"  #Quarternion Stream 16Byte

    ### UUID for SensorTag CC2650
    acclUUID_sensortag = "f000aa80-0451-4000-b000-000000000000"  # Accelerometer Service UUID
    dataUUID_sensortag = "f000aa81-0451-4000-b000-000000000000"  # Characteristics for Accelerometer Data
    ctrlUUID_sensortag = "f000aa82-0451-4000-b000-000000000000"  # Characteristics for Accelerometer Control
    rateUUID_sensortag = "f000aa83-0451-4000-b000-000000000000"  # period (sampling rate)
    readData_sensortag = "<hhhhhhhhh"

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
            self.cmdEnable = "0x7f"   #7f --> 0111 1111 (1(work on mortion) 1(magnet) 111(acc-z,y,x) 111 (gyro-z,y,x))
            self.cmdDisable = "0x0000"
            self.cmdPeriod = "0x0A"

    def connect(self):
        print("connecting to a ", self.vendor, " device: ", self.addr)

        try:
            if (self.vendor == "neblina"):
                self.dev = btle.Peripheral(self.addr, "random")
            elif (self.vendor == "sensortag"):
                self.dev = btle.Peripheral(self.addr, "public")                
        except Exception:
            print("[ERROR] Connection Error occurred! ")
            raise
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
                self.acclCtrl.write(struct.pack("<h", int(self.cmdEnable, 16)))
                self.acclRate.write(struct.pack("<B", int(self.cmdPeriod, 16)))
                #print("successfully set to 100ms for sampling rate")
            

        except Exception:
            print("Accelerometer Service does not exist!")
            self.disconnect()
            raise
        else:
            print("Successfully received accelerometer service from a ", self.vendor, " sensor")
            return True

    def disconnect(self):
        self.dev.disconnect()

    def enable(self):
        if (self.vendor == "neblina"):
            self.acclCtrl.write(struct.pack("<B", 0x01))
        elif (self.vendor == "sensortag"):
            self.acclCtrl.write(struct.pack("<h", int(self.cmdEnable, 16)))

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
        quat = [0] * 4

        SHOW_ACC_DATA = False 

        try:
            data = self.acclData.read()
        except Exception:
            raise

        if (self.vendor == "neblina"):
            if SHOW_ACC_DATA:
                print("DATA: ", data, "SIZE: ", len(data))
            if len(data) == 14:
                header, timestamp, accl[0], accl[1], accl[2] = struct.unpack(self.readData,data)  # self.acclData.read())


        elif (self.vendor == "sensortag"):
            if SHOW_ACC_DATA:
                print("DATA: ", data, "SIZE: ", len(data))
            gyro[0], gyro[1], gyro[2], accl[0], accl[1], accl[2], magn[0], magn[1], magn[2] = struct.unpack(
                self.readData, data)
            
        accl[0] = round((accl[0] * 1.0) / (32768 / 16), 2)  # 16G
        accl[1] = round((accl[1] * 1.0) / (32768 / 16), 2)
        accl[2] = round((accl[2] * 1.0) / (32768 / 16), 2)

        gyro[0] = round((gyro[0] * 1.0) / (65536 / 500), 2) # range: -250, +250
        gyro[1] = round((gyro[1] * 1.0) / (65536 / 500), 2)
        gyro[2] = round((gyro[2] * 1.0) / (65536 / 500), 2)

        if SHOW_ACC_DATA:
            #print("    Acceleration     :  [%4.2f, %4.2f, %4.2f]  %7s" % (accl[0], accl[1], accl[2], self.vendor))
            print("    Acceleration     :  [%5d, %5d, %5d]" % (magn[0], magn[1], magn[2]))

        return accl,gyro,magn
