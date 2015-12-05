import numpy as np
segmentvar = 1500


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

yList = []
file = open("PM25val")
for i in file:
	temp = [float(i)]
	yList.append(temp)

matrixListTrain = []
matrixListTest = []
yListTrain = []
yListTest = []

g_max_n = 1


def normalize(arr):
	max_n_i = np.amax(arr)
	min_n = np.amin(arr)
	mean_n = np.mean(arr)
	g_max_n = max_n
	for i in range(len(TMP)):
		#arr[i] = (arr[i] - mean_n)/(max_n-min_n)
		arr[i] = arr[i]/max_n_i
	return (arr, max_n_i)


max_n = [1,1,1,1]

(TMP, max_n[0]) = normalize(TMP)
(WDIR, max_n[1]) = normalize(WDIR)
(WSPD, max_n[2]) = normalize(WSPD)
(yList, max_n[3]) = normalize(yList)

def normalize_in(arr):
	arr[0] = arr[0]/max_n[0]
	arr[1] = arr[1]/max_n[1]
	arr[2] = arr[2]/max_n[2] 
	return arr

def denormalize(arr):
	return arr*max_n[3]

for i in range(segmentvar):
	yListTrain.append(yList[i])
	temp = []
	temp.append(TMP[i])
	temp.append(WDIR[i])
	temp.append(WSPD[i])
	matrixListTrain.append(temp)
for i in range(segmentvar, len(TMP), 1):
	yListTest.append(yList[i])
	temp = []
	temp.append(TMP[i])
	temp.append(WDIR[i])
	temp.append(WSPD[i])
	matrixListTest.append(temp)



npmatrixListTrain = np.array(matrixListTrain)
npyListTrain = np.array(yListTrain)
npmatrixListTest = np.array(matrixListTest)
npyListTest = np.array(yListTest)
