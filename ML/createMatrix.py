import numpy as np
import random
file = open("RAINval")
RAIN = []
for i in file:
	RAIN.append(float(i))

file = open("RHUMval")
RHUM = []
for i in file:
	RHUM.append(float(i))


file = open("TMPval")
TMP = []
for i in file:
	TMP.append(float(i))

file = open("WDIRval")
WDIR = []
for i in file:
	WDIR.append(float(i))

file = open("WSPDval")
WSPD = []
for i in file:
	WSPD.append(float(i))

matrixList = []
for i in range( len(RAIN) ):
	temp = []
	temp.append(1)
	temp.append(RAIN[i])
	temp.append(RHUM[i])
	temp.append(TMP[i])
	temp.append(WDIR[i])
	temp.append(WSPD[i])
	matrixList.append(temp)
featureMatrix = np.matrix(matrixList)
yMatrixList = []
file = open("O3val")
for i in file:
	temp = [float(i)]
	yMatrixList.append(temp)							# thetaMatrix = 5*1
yMatrix = np.matrix(yMatrixList)        #yMatrix is x*1 and featureMatrix x*5


#start MultiVariate Polynomial regression
thetaMatrix = np.matrix([ [random.uniform(0.0, 1000.0)], [random.uniform(0.0, 1000.0)], [random.uniform(0.0, 1000.0)], [random.uniform(0.0, 1000.0)], [random.uniform(0.0, 1000.0)], [random.uniform(0.0, 1000.0)] ])
def costFunction(x):
	totalErr = 0
	for i in range( len(yMatrix) ):
		hx = featureMatrix[i,] * thetaMatrix 
		totalErr += (hx - yMatrix[i, 0]) ** 2
	return totalErr / (2 * len(yMatrix))
x = np.linalg.inv(featureMatrix.transpose() * featureMatrix) * featureMatrix.transpose() * yMatrix
print  costFunction(x)
print x
for i in range(len(yMatrix)):
	print featureMatrix[i, ] * x


	






