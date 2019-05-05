from decimal import Decimal
import numpy as np
from numpy import array
from numpy.linalg import norm

LEFTARM = 'leftArm'
RIGHTARM = 'rightArm'
LEFTANKLE = 'leftAnkle'
RIGHTANKLE = 'rightAnkle'
CHEST = 'chest'

ACCL = 'acceleration'
GYRO = 'gyroscope'
ACCL = 'acceleration'
GYRO = 'gyroscope'
HR = 'heartrate'
HRV = 'heartratevariablity'
RR = 'respiration'

X = 0
Y = 1
Z = 2
POSITION = [LEFTARM, RIGHTARM, LEFTANKLE, RIGHTANKLE]
NUM_OF_AXIS = 3


class SlidingWindow:
    def __init__(self, windowSize):
        self.sensorData = {}
        for position in POSITION:
            self.sensorData[position] = {}
            self.sensorData[position][ACCL] = {}
            self.sensorData[position][GYRO] = {}
            for axis in range(0, NUM_OF_AXIS):
                self.sensorData[position][ACCL][axis] = []
                self.sensorData[position][GYRO][axis] = []
                for i in range(0, windowSize):
                    self.sensorData[position][ACCL][axis].append(0.0)
                    self.sensorData[position][GYRO][axis].append(0.0)

        self.sensorData[CHEST] = {}
        self.sensorData[CHEST][HR] = []
        self.sensorData[CHEST][HRV] = []
        self.sensorData[CHEST][RR] = []
        for i in range(0, windowSize):
            self.sensorData[CHEST][HR].append(0.0)
            self.sensorData[CHEST][HRV].append(0.0)
            self.sensorData[CHEST][RR].append(0.0)
                    
    def getAllData(self):
        return self.sensorData

    def add(self, oneSampleData):
        self.deleteFirstElement()
       
        for position in self.sensorData.keys():
            if position == CHEST:
                continue
            for axis in range(0, NUM_OF_AXIS):
                self.sensorData[position][ACCL][axis].append(oneSampleData[position][ACCL][axis])
                self.sensorData[position][GYRO][axis].append(oneSampleData[position][GYRO][axis])
                #self.sensorData[name][position][axis].append(1.1)
        self.sensorData[CHEST][HR].append(oneSampleData[CHEST][HR])
        self.sensorData[CHEST][HRV].append(oneSampleData[CHEST][HRV])
        self.sensorData[CHEST][RR].append(oneSampleData[CHEST][RR])

    def deleteFirstElement(self):
        count = 0
        for position in self.sensorData.keys():
            count += 1
            if position == CHEST:
                continue
            for axis in range(0, NUM_OF_AXIS):
                del self.sensorData[position][ACCL][axis][0]
                del self.sensorData[position][GYRO][axis][0]
        del self.sensorData[CHEST][HR][0]
        del self.sensorData[CHEST][HRV][0]
        del self.sensorData[CHEST][RR][0]

    

class SeizureDetection:  
    def __init__(self):
        self.THRESHOLD_RIGHTARM = 1.2
        self.THRESHOLD_RIGHTANKLE = 1.2 

        self.NUM_OF_DATA = 0

    def calculateVector(self, arrayValue):
        vectorArray = []
        for val in arrayValue:
            tempArray = array([val[X], val[Y], val[Z]])
            vectorArray.append(norm(tempArray))
    
        return vectorArray

    def calculateVector2(self, arrayValue):
        vectorArray = []
        arrayValue = arrayValue[-5:]
        for val in arrayValue:
            tempArray = array([val[X], val[Y], val[Z]])
            vectorArray.append(norm(tempArray))
        
        return vectorArray

    def calculateAverage(self, arrayValue):
        total = 0.0

        for val in arrayValue:
            total += val
        avg = total / len(arrayValue)
        #print("AVG: {0}".format(avg))
        return round(avg, 3)


    def calculateVariance(self, arrayValue):
        #print("variance: {0}".format(round(np.var(arrayValue),3)))

        return round(np.var(arrayValue), 3)


    def determine(self, slidingWindow):
        sensorData = slidingWindow.getAllData()    
        self.WINDOW_SIZE = len(sensorData[CHEST][HR])
        if (self.NUM_OF_DATA < self.WINDOW_SIZE):
            self.NUM_OF_DATA += 1
            print("initialize detection algorithm...")
            return False
        
        mergedArrayRightArm = []
        for i in range(0, self.WINDOW_SIZE):
            mergedArrayRightArm.append([sensorData[RIGHTARM][ACCL][X][i], sensorData[RIGHTARM][ACCL][Y][i], sensorData[RIGHTARM][ACCL][Z][i]])
        
        mergedArrayRightAnkle = []
        for i in range(0, self.WINDOW_SIZE):
            mergedArrayRightAnkle.append([sensorData[RIGHTANKLE][ACCL][X][i], sensorData[RIGHTANKLE][ACCL][Y][i], sensorData[RIGHTANKLE][ACCL][Z][i]])
        
        vectorArrayRightArm = self.calculateVector2(mergedArrayRightArm)        
        vectorArrayRightAnkle = self.calculateVector2(mergedArrayRightAnkle)

        vectorRightArm = self.calculateAverage(vectorArrayRightArm)
        vectorRightAnkle = self.calculateAverage(vectorArrayRightAnkle)      

        varianceRightArm = self.calculateVariance(vectorArrayRightArm)
        varianceRightAnkle = self.calculateVariance(vectorArrayRightAnkle)

        print("analyzing data ...")
        print("HR:{0:3d},  varianceRightArm:{1:5.3f},  varianceRightAnkle:{2:5.3f}, vector:{3:5.3f}, vector:{4:5.3f}".format(sensorData[CHEST][HR][-1], varianceRightArm, varianceRightAnkle, vectorRightArm, vectorRightAnkle))
        
        if(sensorData[CHEST][HR][-1] > 100 and varianceRightArm >= self.THRESHOLD_RIGHTARM and varianceRightAnkle >= self.THRESHOLD_RIGHTANKLE and vectorRightArm >= 2.0 and vectorRightAnkle >=2.0 ):
            return True
        else:
            print("............")
            return False

