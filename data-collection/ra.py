#!/usr/bin/python

import binascii
from bluepy import btle
import struct
import math
import time
from datetime import datetime
from decimal import Decimal

import sys
from accsensor import AccSensor
from readsensorinfo import SensorInfo
from SensorPosition import *

SHOW_ACC_DATA = False

class AccDataFile:

    def __init__(self, filename, position):
        sensorinfo = SensorInfo(filename)
        result = sensorinfo.getSensorInfo(position)
        self.vendor = result["vendor"]
        self.addr = result["address"]
        self.position = position
        print ("VENDOR: " + self.vendor)
        print ("IPADDR: " + self.addr)

        self.accsensor = AccSensor(self.vendor, self.addr)


    def saveData(self):
        oldhour = time.strftime("%H")
        while True:
            try:
                self.accdata, self.gyro, self.mag = self.accsensor.read()
            except Exception:
                raise
            else:
                now = datetime.now()
                timestamp = now.strftime("%Y%m%d,%H%M%S")
                decisec = now.strftime("%f")
                timestamp = timestamp + "." + str(round(float("." + decisec[:2]), 1))[-1]
                hour = time.strftime("%H")
                self.datafile.write(timestamp + "," + str(self.accdata[0]) + "," +
                                    str(self.accdata[1]) + "," + str(self.accdata[2]) + "," + str(self.gyro[0]) + "," + str(self.gyro[1]) + "," + str(self.gyro[2]) +  "," + str(self.mag[0]) + "," + str(self.mag[1]) + "," + str(self.mag[2]) + "\n")
                print("[Sensortag Data]  Timestamp: {0},  Accelerometer: {1:7.2f} {2:7.2f} {3:7.2f},  Gyroscope: {4:7.2f} {5:7.2f} {6:7.2f},  Magnetometer: {7:4d} {8:4d} {9:4d}".format(timestamp, self.accdata[0],self.accdata[1], self.accdata[2],self.gyro[0],self.gyro[1],self.gyro[2],self.mag[0],self.mag[1],self.mag[2]))
                

                if oldhour != hour:
                    oldhour = hour
                    self.closeFile()
                    self.createFile()

    def createFile(self):
        print("Data Files are generated")
        self.timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.fname = self.timestr + "_" + self.position + ".csv"
        try:
            self.datafile = open(self.fname, "w")
            print ("WRITE")
        except Exception:
            raise

    def closeFile(self):
        self.datafile.close()

    def connectAccSensor(self):
        try:
            self.accsensor.connect()
        except Exception:
            raise

    def disconnectAccSensor(self):
        self.accsensor.disconnect()

if (__name__ == "__main__"):
    acc = AccDataFile("sensortag-addr.info", RA)

    while True:
        print("Seizure Monitoring System starts...")
        try:
            acc.connectAccSensor()
            acc.createFile()
            acc.saveData()

        except KeyboardInterrupt:
            acc.closeFile()
            acc.disconnectAccSensor()
            sys.exit()

        except Exception:
            acc.closeFile()
            acc.disconnectAccSensor()
            print("***** EXCEPTION OCCURS. PROGRAM RESTARTS... *****")
            #print(str(err))

