
from pyqtgraph import QtGui, QtCore
from PyQt5.QtCore import QRect
import matplotlib.pyplot as plt
import numpy as np
import math
import pyqtgraph as pg
import random
import time
import random
import os
from scipy.misc import imread, imrotate, imresize


WARNING = 0
ALERT   = 1

TIME_SERIES_DATA_SIZE = 100

LEFTARM = 'leftArm'
RIGHTARM = 'rightArm'
LEFTANKLE = 'leftAnkle'
RIGHTANKLE = 'rightAnkle'
CHEST = 'chest'

ACCL = 'acceleration'
GYRO = 'gyroscope'
MAGN = 'magnetometer'
HR = 'heartrate'
HRV = 'heartratevariablity'
RR = 'respiration'

X = 0
Y = 1
Z = 2
AVG = 3

ACCL_Y_HIGH =  4
ACCL_Y_LOW  = -4
GYRO_Y_HIGH =  300
GYRO_Y_LOW  = -300
MAGN_Y_HIGH =  700
MAGN_Y_LOW  = -700


class SensorGraph(object):
    def __init__(self):
        self.accData = {}
        self.accData['1x'] = []
        self.accData['1y'] = []
        self.accData['1z'] = []

        self.data = {}
        self.data[LEFTARM] = {}
        self.data[LEFTARM][ACCL] = {}
        self.data[LEFTARM][ACCL][X] = []
        self.data[LEFTARM][ACCL][Y] = []
        self.data[LEFTARM][ACCL][Z] = []
        self.data[LEFTARM][GYRO] = {}
        self.data[LEFTARM][GYRO][X] = []
        self.data[LEFTARM][GYRO][Y] = []
        self.data[LEFTARM][GYRO][Z] = []
        self.data[LEFTARM][MAGN] = {}
        self.data[LEFTARM][MAGN][X] = []
        self.data[LEFTARM][MAGN][Y] = []
        self.data[LEFTARM][MAGN][Z] = []
        self.data[LEFTARM][ACCL][AVG] = []
        self.data[LEFTARM][GYRO][AVG] = []
        self.data[LEFTARM][MAGN][AVG] = []

        self.data[LEFTANKLE] = {}
        self.data[LEFTANKLE][ACCL] = {}
        self.data[LEFTANKLE][ACCL][X] = []
        self.data[LEFTANKLE][ACCL][Y] = []
        self.data[LEFTANKLE][ACCL][Z] = []
        self.data[LEFTANKLE][GYRO] = {}
        self.data[LEFTANKLE][GYRO][X] = []
        self.data[LEFTANKLE][GYRO][Y] = []
        self.data[LEFTANKLE][GYRO][Z] = []
        self.data[LEFTANKLE][MAGN] = {}
        self.data[LEFTANKLE][MAGN][X] = []
        self.data[LEFTANKLE][MAGN][Y] = []
        self.data[LEFTANKLE][MAGN][Z] = []
        self.data[LEFTANKLE][ACCL][AVG] = []
        self.data[LEFTANKLE][GYRO][AVG] = []
        self.data[LEFTANKLE][MAGN][AVG] = []

        self.data[RIGHTARM] = {}
        self.data[RIGHTARM][ACCL] = {}
        self.data[RIGHTARM][ACCL][X] = []
        self.data[RIGHTARM][ACCL][Y] = []
        self.data[RIGHTARM][ACCL][Z] = []
        self.data[RIGHTARM][GYRO] = {}
        self.data[RIGHTARM][GYRO][X] = []
        self.data[RIGHTARM][GYRO][Y] = []
        self.data[RIGHTARM][GYRO][Z] = []
        self.data[RIGHTARM][MAGN] = {}
        self.data[RIGHTARM][MAGN][X] = []
        self.data[RIGHTARM][MAGN][Y] = []
        self.data[RIGHTARM][MAGN][Z] = []
        self.data[RIGHTARM][ACCL][AVG] = []
        self.data[RIGHTARM][GYRO][AVG] = []
        self.data[RIGHTARM][MAGN][AVG] = []

        self.data[RIGHTANKLE] = {}
        self.data[RIGHTANKLE][ACCL] = {}
        self.data[RIGHTANKLE][ACCL][X] = []
        self.data[RIGHTANKLE][ACCL][Y] = []
        self.data[RIGHTANKLE][ACCL][Z] = []
        self.data[RIGHTANKLE][GYRO] = {}
        self.data[RIGHTANKLE][GYRO][X] = []
        self.data[RIGHTANKLE][GYRO][Y] = []
        self.data[RIGHTANKLE][GYRO][Z] = []
        self.data[RIGHTANKLE][MAGN] = {}
        self.data[RIGHTANKLE][MAGN][X] = []
        self.data[RIGHTANKLE][MAGN][Y] = []
        self.data[RIGHTANKLE][MAGN][Z] = []
        self.data[RIGHTANKLE][ACCL][AVG] = []
        self.data[RIGHTANKLE][GYRO][AVG] = []
        self.data[RIGHTANKLE][MAGN][AVG] = []

        self.data[CHEST] = {}
        self.data[CHEST][HR] = []
        self.data[CHEST][HRV] = []
        self.data[CHEST][RR] = []
      
      # beep sound
        self.duration = 0.5
        self.freq = 440

        self.initializeAccData()

        self.app = QtGui.QApplication([])
        pg.setConfigOption('background', 'w')
        self.win = pg.GraphicsWindow(size=(1920,1024))
        self.win.setWindowTitle('***  SEIZURE MONITORING SYTEM  ***')

        self.titlePlot = self.win.addPlot(0, 0, colspan=2)
        self.titlePlot.hideAxis('left')
        self.titlePlot.hideAxis('bottom')
        text="seizure monitoring system"
        titleHTML = '<div style="text-align: center"><span style="color: purple; font-size: 23pt; font-weight:bold;">' + text + '</span></div>'
        self.systemTitle = pg.TextItem(text, color=(255, 0, 0), html=titleHTML, anchor=(0.5, 0.5), border=None, \
                          fill=None, angle=0, rotateAxis=None)
        self.titlePlot.addItem(self.systemTitle)

        gl_mh = self.win.addLayout(0, 0)
        vb_mh = gl_mh.addViewBox(0, 0, enableMouse=False)
        vb_mh.setRange(xRange=(0, 600), yRange=(0, 60))
        #vb_mh.addItem(logo_mohawk)
        gl_mh.addViewBox(1, 0)

        # add plot for each axis
        self.dataPlot = {}
        self.dataPlot[LEFTARM] = {}        
        self.dataPlot[LEFTARM][ACCL] = self.win.addPlot(1,0)
        self.dataPlot[LEFTARM][GYRO] = self.win.addPlot(2,0)
        self.dataPlot[LEFTARM][MAGN] = self.win.addPlot(3,0)

        self.dataPlot_L1 = self.win.addPlot(4, 0, colspan=2)
        self.dataPlot_L1.hideAxis('left')
        self.dataPlot_L1.hideAxis('bottom')
        self.dataPlot_L1.addLine(y=10)

        self.dataPlot[LEFTANKLE] = {}        
        self.dataPlot[LEFTANKLE][ACCL] = self.win.addPlot(5,0)
        self.dataPlot[LEFTANKLE][GYRO] = self.win.addPlot(6,0)
        self.dataPlot[LEFTANKLE][MAGN] = self.win.addPlot(7,0)


        self.dataPlot[RIGHTARM] = {}        
        self.dataPlot[RIGHTARM][ACCL] = self.win.addPlot(1,1)
        self.dataPlot[RIGHTARM][GYRO] = self.win.addPlot(2,1)
        self.dataPlot[RIGHTARM][MAGN] = self.win.addPlot(3,1)

        self.dataPlot[RIGHTANKLE] = {}        
        self.dataPlot[RIGHTANKLE][ACCL] = self.win.addPlot(5,1)
        self.dataPlot[RIGHTANKLE][GYRO] = self.win.addPlot(6,1)
        self.dataPlot[RIGHTANKLE][MAGN] = self.win.addPlot(7,1)

        self.dataPlot_L2 = self.win.addPlot(8, 0, colspan=2)
        self.dataPlot_L2.hideAxis('left')
        self.dataPlot_L2.hideAxis('bottom')
        self.dataPlot_L2.addLine(y=10)

        self.dataPlot[CHEST+HR] = self.win.addPlot(9,0)
        self.dataPlot[CHEST+RR+HRV] = self.win.addPlot(9,1)
        
        
        self.bottomPlot = self.win.addPlot(10, 0, colspan=2)
        self.bottomPlot.hideAxis('left')
        self.bottomPlot.hideAxis('bottom')

        self.waitingText = 'detecting Seizure...'
        self.msgWarning = pg.TextItem(self.waitingText, color=(255, 0, 0), html=None, anchor=(0.5, 0.3), border=None, \
                          fill=None, angle=0, rotateAxis=None)        
        self.bottomPlot.addItem(self.msgWarning)


        # set title of each axis
        self.dataPlot[LEFTARM][ACCL].setTitle('<span style="font-color:black; font-weight: bold;"> LEFT ARM ACCELERATOR </span>')
        self.dataPlot[LEFTARM][GYRO].setTitle('<span style="font-color:black; font-weight: bold;"> LEFT ARM GYROSCOPE </span>')
        self.dataPlot[LEFTARM][MAGN].setTitle('<span style="font-color:black; font-weight: bold;"> LEFT ARM MAGNOMETER </span>')

        self.dataPlot[LEFTANKLE][ACCL].setTitle('<span style="font-color:black; font-weight: bold;"> LEFT ANKLE ACCELERATOR </span>')
        self.dataPlot[LEFTANKLE][GYRO].setTitle('<span style="font-color:black; font-weight: bold;"> LEFT ANKLE GYROSCOPE </span>')
        self.dataPlot[LEFTANKLE][MAGN].setTitle('<span style="font-color:black; font-weight: bold;"> LEFT ANKLE MAGNOMETER </span>')

        self.dataPlot[RIGHTARM][ACCL].setTitle('<span style="font-color:black; font-weight: bold;"> RIGHT ARM ACCELERATOR </span>')
        self.dataPlot[RIGHTARM][GYRO].setTitle('<span style="font-color:black; font-weight: bold;"> RIGHT ARM GYROSCOPE </span>')
        self.dataPlot[RIGHTARM][MAGN].setTitle('<span style="font-color:black; font-weight: bold;"> RIGHT ARM MAGNOMETER </span>')

        self.dataPlot[RIGHTANKLE][ACCL].setTitle('<span style="font-color:black; font-weight: bold;"> RIGHT ANKLE ACCELERATOR </span>')
        self.dataPlot[RIGHTANKLE][GYRO].setTitle('<span style="font-color:black; font-weight: bold;"> RIGHT ANKLE GYROSCOPE </span>')
        self.dataPlot[RIGHTANKLE][MAGN].setTitle('<span style="font-color:black; font-weight: bold;"> RIGHT ANKLE MAGNOMETER </span>')

        self.dataPlot[CHEST+HR].setTitle('<span style="font-color:black; font-weight: bold;"> HEART RATE </span>')
        self.dataPlot[CHEST+RR+HRV].setTitle('<span style="font-color:black; font-weight: bold;"> RESPIRATION & HRV </span>')

        # set range of each graph
        self.dataPlot[LEFTARM][ACCL].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[LEFTARM][GYRO].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[LEFTARM][MAGN].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)

        self.dataPlot[LEFTANKLE][ACCL].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[LEFTANKLE][GYRO].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[LEFTANKLE][MAGN].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)

        self.dataPlot[RIGHTARM][ACCL].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[RIGHTARM][GYRO].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[RIGHTARM][MAGN].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)

        self.dataPlot[RIGHTANKLE][ACCL].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[RIGHTANKLE][GYRO].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)
        self.dataPlot[RIGHTANKLE][MAGN].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)

        self.dataPlot[CHEST+HR].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)      
        self.dataPlot[CHEST+RR+HRV].setXRange(0, TIME_SERIES_DATA_SIZE, padding=0)

        self.dataPlot[LEFTARM][ACCL].setYRange(ACCL_Y_LOW, ACCL_Y_HIGH, padding=0)
        self.dataPlot[LEFTARM][GYRO].setYRange(GYRO_Y_LOW, GYRO_Y_HIGH, padding=0)
        self.dataPlot[LEFTARM][MAGN].setYRange(MAGN_Y_LOW, MAGN_Y_HIGH, padding=0)

        self.dataPlot[LEFTANKLE][ACCL].setYRange(ACCL_Y_LOW, ACCL_Y_HIGH, padding=0)
        self.dataPlot[LEFTANKLE][GYRO].setYRange(GYRO_Y_LOW, GYRO_Y_HIGH, padding=0)
        self.dataPlot[LEFTANKLE][MAGN].setYRange(MAGN_Y_LOW, MAGN_Y_HIGH, padding=0)

        self.dataPlot[RIGHTARM][ACCL].setYRange(ACCL_Y_LOW, ACCL_Y_HIGH, padding=0)
        self.dataPlot[RIGHTARM][GYRO].setYRange(GYRO_Y_LOW, GYRO_Y_HIGH, padding=0)
        self.dataPlot[RIGHTARM][MAGN].setYRange(MAGN_Y_LOW, MAGN_Y_HIGH, padding=0)

        self.dataPlot[RIGHTANKLE][ACCL].setYRange(ACCL_Y_LOW, ACCL_Y_HIGH, padding=0)
        self.dataPlot[RIGHTANKLE][GYRO].setYRange(GYRO_Y_LOW, GYRO_Y_HIGH, padding=0)
        self.dataPlot[RIGHTANKLE][MAGN].setYRange(MAGN_Y_LOW, MAGN_Y_HIGH, padding=0)

        self.dataPlot[CHEST+HR].setYRange(0, 150, padding=0)
        self.dataPlot[CHEST+RR+HRV].setYRange(0, 80, padding=0)

        # set the color of line
        self.dataCurve = {}
        
        self.dataCurve[LEFTARM] = {}
        self.dataCurve[LEFTARM][ACCL] = self.dataPlot[LEFTARM][ACCL].plot(pen=(255,0,0), name="AVG")
        self.dataCurve[LEFTARM][GYRO] = self.dataPlot[LEFTARM][GYRO].plot(pen=(0, 255, 0), name="AVG")
        self.dataCurve[LEFTARM][MAGN] = self.dataPlot[LEFTARM][MAGN].plot(pen=(0, 0, 255), name="AVG")

        self.dataCurve[LEFTANKLE] = {}
        self.dataCurve[LEFTANKLE][ACCL] = self.dataPlot[LEFTANKLE][ACCL].plot(pen=(255, 0, 0), name="AVG")
        self.dataCurve[LEFTANKLE][GYRO] = self.dataPlot[LEFTANKLE][GYRO].plot(pen=(0, 255, 0), name="AVG")
        self.dataCurve[LEFTANKLE][MAGN] = self.dataPlot[LEFTANKLE][MAGN].plot(pen=(0, 0, 255), name="AVG")

        self.dataCurve[RIGHTARM] = {}

        self.dataCurve[RIGHTARM][ACCL] = self.dataPlot[RIGHTARM][ACCL].plot(pen=(255, 0, 0), name="AVG")
        self.dataCurve[RIGHTARM][GYRO] = self.dataPlot[RIGHTARM][GYRO].plot(pen=(0, 255, 0), name="AVG")
        self.dataCurve[RIGHTARM][MAGN] = self.dataPlot[RIGHTARM][MAGN].plot(pen=(0, 0, 255), name="AVG")

        self.dataCurve[RIGHTANKLE] = {}
        self.dataCurve[RIGHTANKLE][ACCL] = self.dataPlot[RIGHTANKLE][ACCL].plot(pen=(255, 0, 0), name="AVG")
        self.dataCurve[RIGHTANKLE][GYRO] = self.dataPlot[RIGHTANKLE][GYRO].plot(pen=(0, 255, 0), name="AVG")
        self.dataCurve[RIGHTANKLE][MAGN] = self.dataPlot[RIGHTANKLE][MAGN].plot(pen=(0, 0, 255), name="AVG")

        self.dataCurve[CHEST] = {}
        self.dataCurve[CHEST][HR] = self.dataPlot[CHEST+HR].plot(pen=(255,0,0), name="HR")

        self.dataCurve[CHEST][HRV] = self.dataPlot[CHEST+RR+HRV].plot(pen=(0, 255,0), name="HRV")
        self.dataCurve[CHEST][RR] = self.dataPlot[CHEST+RR+HRV].plot(pen=(0,0,255), name="RR")

        
    def initializeAccData(self):
        # set initial data to 0

        for col in range(0, TIME_SERIES_DATA_SIZE):
            self.accData['1x'].append(0.0)

        for col in range(0, TIME_SERIES_DATA_SIZE):
            self.accData['1y'].append(0.0)

        for col in range(0, TIME_SERIES_DATA_SIZE):
            self.accData['1z'].append(0.0)

        for i in range(0, TIME_SERIES_DATA_SIZE):
            self.data[LEFTARM][ACCL][AVG].append(0.0)
            self.data[LEFTARM][GYRO][AVG].append(0.0)
            self.data[LEFTARM][MAGN][AVG].append(0.0)

            self.data[RIGHTARM][ACCL][AVG].append(0.0)
            self.data[RIGHTARM][GYRO][AVG].append(0.0)
            self.data[RIGHTARM][MAGN][AVG].append(0.0)

            self.data[LEFTANKLE][ACCL][AVG].append(0.0)
            self.data[LEFTANKLE][GYRO][AVG].append(0.0)
            self.data[LEFTANKLE][MAGN][AVG].append(0.0)

            self.data[RIGHTANKLE][ACCL][AVG].append(0.0)
            self.data[RIGHTANKLE][GYRO][AVG].append(0.0)
            self.data[RIGHTANKLE][MAGN][AVG].append(0.0)

        for i in range(0, TIME_SERIES_DATA_SIZE):
            self.data[CHEST][HR].append(0)
            self.data[CHEST][HRV].append(0)
            self.data[CHEST][RR].append(0)


    def update(self, oneSample):
        self.deleteFirstElement()
        self.addNewElement(oneSample)
        self.setDataOnPlot()

        self.app.processEvents()

    def setDataOnPlot(self):
        self.dataCurve[LEFTARM][ACCL].setData(self.data[LEFTARM][ACCL][AVG])
        self.dataCurve[LEFTARM][GYRO].setData(self.data[LEFTARM][GYRO][AVG])
        self.dataCurve[LEFTARM][MAGN].setData(self.data[LEFTARM][MAGN][AVG])

        self.dataCurve[LEFTANKLE][ACCL].setData(self.data[LEFTANKLE][ACCL][AVG])
        self.dataCurve[LEFTANKLE][GYRO].setData(self.data[LEFTANKLE][GYRO][AVG])
        self.dataCurve[LEFTANKLE][MAGN].setData(self.data[LEFTANKLE][MAGN][AVG])

        self.dataCurve[RIGHTARM][ACCL].setData(self.data[RIGHTARM][ACCL][AVG])
        self.dataCurve[RIGHTARM][GYRO].setData(self.data[RIGHTARM][GYRO][AVG])
        self.dataCurve[RIGHTARM][MAGN].setData(self.data[RIGHTARM][MAGN][AVG])

        self.dataCurve[RIGHTANKLE][ACCL].setData(self.data[RIGHTANKLE][ACCL][AVG])
        self.dataCurve[RIGHTANKLE][GYRO].setData(self.data[RIGHTANKLE][GYRO][AVG])
        self.dataCurve[RIGHTANKLE][MAGN].setData(self.data[RIGHTANKLE][MAGN][AVG])

        self.dataCurve[CHEST][HR].setData(self.data[CHEST][HR])
        self.dataCurve[CHEST][HRV].setData(self.data[CHEST][HRV])
        self.dataCurve[CHEST][RR].setData(self.data[CHEST][RR])

    def addNewElement(self, oneSample):
        self.data[LEFTARM][ACCL][AVG].append(
            round((oneSample[LEFTARM][ACCL][X] + oneSample[LEFTARM][ACCL][Y] + oneSample[LEFTARM][ACCL][Z]) / 3, 2))
        self.data[LEFTARM][GYRO][AVG].append(
            round((oneSample[LEFTARM][GYRO][X] + oneSample[LEFTARM][GYRO][Y] + oneSample[LEFTARM][GYRO][Z]) / 3, 2))
        self.data[LEFTARM][MAGN][AVG].append(
            round((oneSample[LEFTARM][MAGN][X] + oneSample[LEFTARM][MAGN][Y] + oneSample[LEFTARM][MAGN][Z]) / 3, 2))

        self.data[RIGHTARM][ACCL][AVG].append(
            round((oneSample[RIGHTARM][ACCL][X] + oneSample[RIGHTARM][ACCL][Y] + oneSample[RIGHTARM][ACCL][Z]) / 3, 2))
        self.data[RIGHTARM][GYRO][AVG].append(
            round((oneSample[RIGHTARM][GYRO][X] + oneSample[RIGHTARM][GYRO][Y] + oneSample[RIGHTARM][GYRO][Z]) / 3, 2))
        self.data[RIGHTARM][MAGN][AVG].append(
            round((oneSample[RIGHTARM][MAGN][X] + oneSample[RIGHTARM][MAGN][Y] + oneSample[RIGHTARM][MAGN][Z]) / 3, 2))

        self.data[LEFTANKLE][ACCL][AVG].append(
            round((oneSample[LEFTANKLE][ACCL][X] + oneSample[LEFTANKLE][ACCL][Y] + oneSample[LEFTANKLE][ACCL][Z]) / 3, 2))
        self.data[LEFTANKLE][GYRO][AVG].append(
            round((oneSample[LEFTANKLE][GYRO][X] + oneSample[LEFTANKLE][GYRO][Y] + oneSample[LEFTANKLE][GYRO][Z]) / 3, 2))
        self.data[LEFTANKLE][MAGN][AVG].append(
            round((oneSample[LEFTANKLE][MAGN][X] + oneSample[LEFTANKLE][MAGN][Y] + oneSample[LEFTANKLE][MAGN][Z]) / 3, 2))

        self.data[RIGHTANKLE][ACCL][AVG].append(
            round((oneSample[RIGHTANKLE][ACCL][X] + oneSample[RIGHTANKLE][ACCL][Y] + oneSample[RIGHTANKLE][ACCL][Z]) / 3, 2))
        self.data[RIGHTANKLE][GYRO][AVG].append(
            round((oneSample[RIGHTANKLE][GYRO][X] + oneSample[RIGHTANKLE][GYRO][Y] + oneSample[RIGHTANKLE][GYRO][Z]) / 3, 2))
        self.data[RIGHTANKLE][MAGN][AVG].append(
            round((oneSample[RIGHTANKLE][MAGN][X] + oneSample[RIGHTANKLE][MAGN][Y] + oneSample[RIGHTANKLE][MAGN][Z]) / 3, 2))

        self.data[CHEST][HR].append(oneSample[CHEST][HR])
        self.data[CHEST][HRV].append(oneSample[CHEST][HRV])
        self.data[CHEST][RR].append(oneSample[CHEST][RR])
 

    def deleteFirstElement(self):
        del self.data[LEFTARM][ACCL][AVG][0]
        del self.data[LEFTARM][GYRO][AVG][0]
        del self.data[LEFTARM][MAGN][AVG][0]

        del self.data[LEFTANKLE][ACCL][AVG][0]
        del self.data[LEFTANKLE][GYRO][AVG][0]
        del self.data[LEFTANKLE][MAGN][AVG][0]

        del self.data[RIGHTARM][ACCL][AVG][0]
        del self.data[RIGHTARM][GYRO][AVG][0]
        del self.data[RIGHTARM][MAGN][AVG][0]

        del self.data[RIGHTANKLE][ACCL][AVG][0]
        del self.data[RIGHTANKLE][GYRO][AVG][0]
        del self.data[RIGHTANKLE][MAGN][AVG][0]

        del self.data[CHEST][HR][0]
        del self.data[CHEST][HRV][0]
        del self.data[CHEST][RR][0]



    def displayTitle(self):
        titleHTML = '<div style="text-align: center"><span style="color: #FF0; font-size: 20pt;">SEIZURE SYMPTOM MONITOR</span></div>'
        self.systemTitle.setHtml(titleHTML)

    def displayAlarm(self):
        '''
        textHTML = '<div style="text-align: center"><span style="color: #000; font-size: 20pt">'
        textHTML += "Alert - Seizure Left Ankle Symptom  <br>"
        '''

        textHTML = '<div style="text-align: center"><span style="color: #F00; font-size: 20pt">'
        textHTML += "WARNING - SEIZURE! SEIZURE! SEIZURE!  </span></div> <br>"

        self.msgWarning.setHtml(textHTML)

        # generate beep sound
        for i in range(0, 2):
            os.system('play -nq -t alsa synth %s sine %f' % (self.duration, self.freq))
            
    def displayNormal(self):
        self.msgWarning.setHtml(self.waitingText)

def main():
    ag = SensorGraph()                 

if (__name__ == "__main__"):
    main()







