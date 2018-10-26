import matplotlib.pyplot as plt
import pandas as pd
import math
D0 = 1
accessPoint = [0,0]
PT = -13.7
PL_d0 = 20.3
Pd0 = [0,1]


def calc_distance(pointA , pointB):
	xx = (abs(pointA[0] - pointB[0]))**2
	yy = (abs(pointA[1] - pointB[1]))**2
	return math.sqrt(xx + yy)


def readData():
	datafile = pd.read_csv("logRssi.csv")
	return datafile


#parse data into 2 lists
def create_list(datafile):
	points = []
	RSSI = []
	for i in range(len(datafile)):
		x = datafile['xCol'][i]
		y = datafile['yRow'][i]
		rssi = datafile['Rssi'][i]
		points.append([x,y])
		RSSI.append(rssi)
	return points,RSSI


def calc_n(points , RSSI):
	nValues = []
	d0 = calc_distance(Pd0 , accessPoint)
	for i in range(len(points)):
		d = calc_distance(points[i] , accessPoint)
		Pr = RSSI[i]
		ratio = d/d0
		if ratio != 1:
			n = (PT - Pr - PL_d0)/(10*(math.log(d/d0 , 10)))
		else:
			n = 0
		nValues.append(n)
	return nValues


#average n value
def calc_avg_n(nValues):
	sum = 0
	for i in range(len(nValues)):
		sum = sum + nValues[i]
	avg = sum/len(nValues)
	return avg


def zerolistmaker(n):
	listofzeros = [0] * n
	return listofzeros


#draws a plot n_D
def draw(nValues , points):
	distanceList = []
	for i in range(len(points)):
		d = calc_distance(points[i] , accessPoint)
		distanceList.append(d)
		text = plt.text(d, nValues[i], "%.2f" % round(nValues[i],2))  
	plt.plot(distanceList, nValues, 'r^')
	plt.axis([0, max(distanceList)+1, 0, max(nValues)+1])
	plt.xlabel('Distances')
	plt.ylabel('n parameter')
	plt.show()


# divides points into several lists according to the number of breakpoints
# and returns a list of lists of points
# and their rss values
def breakPointModel(points , RSSI , brpoints):
	brNumber = len(brpoints)
	flags = zerolistmaker(len(points))
	lists = {}
	rssValues = {}
	for i in range(brNumber+1):
		lists['l'+str(i)] = []
		rssValues['l'+str(i)] = []
		for k in range(len(points)):
			if flags[k] == 0:
				dis = calc_distance(points[k] , accessPoint)
				if i < brNumber:
					if dis < brpoints[i]:
						lists['l'+str(i)].append(points[k])
						rssValues['l'+str(i)].append(RSSI[k])
						flags[k] = 1
				else:
					lists['l'+str(i)].append(points[k])
					rssValues['l'+str(i)].append(RSSI[k])		

	#for i in range(len(lists)):
	#	print lists['l'+str(i)] , rssValues['l'+str(i)]
	return lists , rssValues


# calculates n parameter for a breakpoint model
# lists is a list of lists, each containing some points
# rssValues is rss of these points
def calc_brModel_n(lists,rssValues):
	n_sigmaList = []
	for i in range(len(lists)):
		nValues = calc_n(lists['l'+str(i)] , rssValues['l'+str(i)])
		#print nValues , "nvalues"
		draw(nValues , lists['l'+str(i)])
		avg_n = calc_avg_n(nValues)
		sigma = calc_sigma(nValues , avg_n)
		n_sigmaList.append([avg_n , sigma])
	return n_sigmaList


# calculates sigma for n values
def calc_sigma(nValues , avg_n):
	sum = 0
	for i in range(len(nValues)):
		sum = sum + (nValues[i] - avg_n)**2
	variance = sum/len(nValues)
	sigma = math.sqrt(variance)
	return sigma


def main():
	datafile = readData()
	points,RSSI = create_list(datafile)
	nValues = calc_n(points , RSSI)
	avg_n = calc_avg_n(nValues)
	sigma = calc_sigma(nValues , avg_n)
	print avg_n , sigma
	lists,rssValues = breakPointModel(points , RSSI , [5 , 7 , 9 , 10])
	#n_sigmaList = calc_brModel_n(lists , rssValues)
	#for i in range(len(n_sigmaList)):
	#	print n_sigmaList[i]
	draw(nValues , points)


if __name__ == "__main__":
	main()