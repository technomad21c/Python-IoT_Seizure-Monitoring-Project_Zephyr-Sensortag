from bleSensor import *
from time import gmtime, strftime
from sensorGraph import *
from readCsv import ReadCSV
from seizureDetection import SlidingWindow, SeizureDetection
from subprocess import Popen
import sys
import time

WITH_GRIGHTARMPH = True

LEFTARM = 'leftArm'
RIGHTARM = 'rightArm'
LEFTANKLE = 'leftAnkle'
RIGHTANKLE = 'rightAnkle'

ACCL = 'acceleration'
GYRO = 'gyroscope'
ACCL = 'acceleration'
GYRO = 'gyroscope'
MAGN = 'magnetometer'
HR = 'heartrate'
HRV = 'heartratevariablity'
RR = 'respiration'

X = 0
Y = 1
Z = 2

class Monitoring(object):
    def __init__(self):        
        self.sensortag = {}
        self.sensortag[LEFTARM]    = BleSensor('sensortag', '24:71:89:bc:59:80')
        self.sensortag[RIGHTARM]   = BleSensor('sensortag', '54:6c:0e:53:3a:0a')
        self.sensortag[LEFTANKLE]  = BleSensor('sensortag', '54:6c:0e:53:3e:e6')
        self.sensortag[RIGHTANKLE] = BleSensor('sensortag', 'b0:b4:48:ed:cc:05')
        self.DATA_NUM_TO_DETECT_SEIZURE = 20
        

    def setSensorGraph(self):
        print("Sensor graph starts")
        self.sensorGraph = SensorGraph()
        print("Sensor graph ends")

    def connectSensors(self):
        self.sensortag[LEFTARM].connect()
        self.sensortag[RIGHTARM].connect()
        self.sensortag[LEFTANKLE].connect()
        self.sensortag[RIGHTANKLE].connect()

        #Popen(['python', 'zephyrForGraph.py'])

    def close(self):
        self.datafile.close()
        self.disconnectSensors()

    # disconnect sensors
    def disconnectSensors(self):
        self.sensortag[LEFTARM].disconnect()
        self.sensortag[RIGHTARM].disconnect()
        self.sensortag[LEFTANKLE].disconnect()
        self.sensortag[RIGHTANKLE].disconnect()

    def visualize(self):
        slidingData = SlidingWindow(self.DATA_NUM_TO_DETECT_SEIZURE)
        seizure = SeizureDetection()

        data = {}
        data[LEFTARM] = {}
        data[LEFTARM][ACCL] = []
        data[LEFTARM][GYRO] = []
        data[LEFTARM][MAGN] = []
        data[LEFTANKLE] = {}
        data[LEFTANKLE][ACCL] = []
        data[LEFTANKLE][GYRO] = []
        data[LEFTANKLE][MAGN] = []
        data[RIGHTARM] = {}
        data[RIGHTARM][ACCL] = []
        data[RIGHTARM][GYRO] = []
        data[RIGHTARM][MAGN] = []
        data[RIGHTANKLE] = {}
        data[RIGHTANKLE][ACCL] = []
        data[RIGHTANKLE][GYRO] = []
        data[RIGHTANKLE][MAGN] = []
        data[CHEST] = {}
        
        zephyrFile = 'zephyr.csv'

        # fn = time.strftime(LEFTARM + ".csv")
        # self.datafile = open(fn, "w")
        while(True):
            # draw time series acceleration data on screen
            
            data[LEFTARM][ACCL], data[LEFTARM][GYRO], data[LEFTARM][MAGN] = self.sensortag[LEFTARM].read()
            data[RIGHTARM][ACCL], data[RIGHTARM][GYRO], data[RIGHTARM][MAGN] = self.sensortag[RIGHTARM].read()
            data[LEFTANKLE][ACCL], data[LEFTANKLE][GYRO], data[LEFTANKLE][MAGN]  = self.sensortag[LEFTANKLE].read()
            data[RIGHTANKLE][ACCL], data[RIGHTANKLE][GYRO], data[RIGHTANKLE][MAGN] = self.sensortag[RIGHTANKLE].read()

            timestamp = time.strftime("%Y%m%d,%H%M%S")
            # self.datafile.write(timestamp + "," + str(data[LEFTARM][ACCL][X]) + "," + str(data[LEFTARM][ACCL][Y]) + "," + str(data[LEFTARM][ACCL][Z]) + "," + str(data[LEFTARM][GYRO][X]) + "," + str(data[LEFTARM][GYRO][Y]) + "," + str(data[LEFTARM][GYRO][Z]) + "\n")
            # print(timestamp + "," + str(data[LEFTARM][ACCL][X]) + "," + str(data[LEFTARM][ACCL][Y]) + "," + str(data[LEFTARM][ACCL][Z]) + "," + str(data[LEFTARM][GYRO][X]) + "," + str(data[LEFTARM][GYRO][Y]) + "," + str(data[LEFTARM][GYRO][Z]) + "\n")

            zephyr = ReadCSV()
            zephyr.open(zephyrFile)            
            zephyrData = zephyr.readOne()
            zephyr.close()   
            
            data[CHEST][HR]  = zephyrData[0]
            data[CHEST][RR]  = zephyrData[1]
            data[CHEST][HRV]  = zephyrData[2]
           
            self.sensorGraph.update(data)

if(__name__ == "__main__"):

    try:
        m = Monitoring()
        m.connectSensors()        
        if WITH_GRIGHTARMPH:
            m.setSensorGraph()                
        m.visualize()
    except KeyboardInterrupt:
        m.close()
        sys.exit()
    except Exception as err:
        m.close()
        print(str(err))








