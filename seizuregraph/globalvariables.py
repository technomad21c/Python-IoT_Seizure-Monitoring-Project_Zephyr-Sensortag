global LEFTARM
LEFTARM = 'leftArm'
global RIGHTARM
RIGHTARM = 'rightArm'
global LEFTANKLE
LEFTANKLE = 'leftAnkle'
global RIGHTANKLE
RIGHTANKLE = 'rightAnkle'
global CHEST
CHEST = 'chest'
global ACCL
ACCL = 'acceleration'
global GYRO
GYRO = 'gyroscope'
global HR
HR = 'heartrate'
global HRV
HRV = 'heartratevariablity'
global RR
RR = 'respiration'

global X
X = 0
global Y
Y = 1
global Z 
Z= 2 

global data
data = {}
data[LEFTARM] = {}
data[LEFTARM][ACCL] = []
data[LEFTARM][GYRO] = []
data[LEFTANKLE] = {}
data[LEFTANKLE][ACCL] = []
data[LEFTANKLE][GYRO] = []
data[RIGHTARM] = {}
data[RIGHTARM][ACCL] = []
data[RIGHTARM][GYRO] = []
data[RIGHTANKLE] = {}
data[RIGHTANKLE][ACCL] = []
data[RIGHTANKLE][GYRO] = []
data[CHEST] = {}