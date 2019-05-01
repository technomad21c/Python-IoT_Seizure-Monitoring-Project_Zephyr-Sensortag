#!/usr/bin/python

from bluepy import btle
from time import gmtime, strftime
import sys
import time
import struct

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

        filename = time.strftime("%Y%m%d-%H%M%S") + "_chest.csv"
        self.file = open(filename, "w")

    def handleNotification(self, cHandle, data):
        ver, status, hr, rr, temp, posture, activity, hrv, battery, hrc, brc, heatstresslevel, physiologialstrainindex, coretemp = struct.unpack("<bhbhhhhhbbbbbb", data)
        
        if hr < 0 :
            hr = 127 + (127 + hr)
        
        print("Heat Rate: {0}, Respiration Rate: {1}, HRV: {2}, Activity: {3}, Battery: {4}".format(hr, rr / 10, hrv, activity, battery))

        timestamp = time.strftime("%Y%m%d,%H%M%S")
        self.file.write(timestamp + "," + str(hr) + "," + str(rr/10) + "," + str(hrv) + "\n")

    def close(self):
        self.file.close()

if(__name__ == "__main__"):
    try:
        #p = btle.Peripheral("a0:e6:f8:fa:91:b2", btle.ADDR_TYPE_PUBLIC)
        p = btle.Peripheral("a0:e6:f8:ef:ff:56", btle.ADDR_TYPE_PUBLIC)
        p.setDelegate( MyDelegate() )

        # Setup to turn notifications on, e.g.
        svc = p.getServiceByUUID( "befdff20-c979-11e1-9b21-0800200c9a66" )
        ch = svc.getCharacteristics()[0]
        print(ch)
        print(ch.valHandle)

        p.writeCharacteristic(ch.valHandle+1, "\x01\x00")

        while True:
            if p.waitForNotifications(1.0):
            # handleNotification() was called
                continue

    except KeyboardInterrupt:
       p.close()
       print "program terminated!"
       sys.exit() 
