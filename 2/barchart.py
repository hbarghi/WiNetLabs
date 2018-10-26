import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.transforms as mtransforms
from matplotlib.transforms import offset_copy
from random import randint


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        #print height
        plt.text(rect.get_x() + rect.get_width()/2., (-1.05)*height,
                '%d' % int(-height),
                ha='center', va='bottom')


def draw(AP ,STDDEV):
	menMeans = (20, 35, 30, 35, 27)
	ind = np.arange(len(AP))    # the x locations for the groups
	width = 0.35       # the width of the bars: can also be len(x) sequence
	p1 = plt.bar(ind, AP.values(), width, color='r')
	p2 = plt.bar(ind, STDDEV.values(), width, bottom=AP.values(), color='b')
	plt.ylabel('Signal Strength')
	plt.title('APs and RSSI')
	plt.xticks(ind, AP)
	plt.yticks(np.arange(-100, 0, 10))
	plt.legend((p1[0], p2[0]), ('RSSI', 'STDDEV'))
	autolabel(p1)
	plt.show()


def parser():  #parsing input file
	List = []
	f = open("myhome/y/c.txt")
	data = f.readlines()
	f.close()
	for d in data:
	    part = d.split()
	    if(len(part) == 3):
	    	name = part[1]
	    	rssi = part[2]
	    	List.append((name , int(rssi)))
	return List


def calc(List):
	dict1 = {}  #sum and mean
	dict2 = {}  #N
	dict3 = {}	#stddev
	diff = []

	for item in List:
		if(item[0] not in dict1):
			dict1[item[0]] = item[1]
			dict2[item[0]] = 1
		elif(item[0] in dict1):
			dict1[item[0]] = dict1[item[0]] + item[1]
			dict2[item[0]] = dict2[item[0]] + 1

	for d in dict1:
		dict1[d] = dict1[d] / dict2[d]

	for item in List:             
		if(item[0] in dict1):
			mean = dict1[item[0]]
			dif = (item[1] - mean)**2
			diff.append((item[0],dif))

	for item in diff:             #calculate the sumation of diff
		if(item[0] not in dict3):
			dict3[item[0]] = item[1]
		elif(item[0] in dict3):
			dict3[item[0]] = dict3[item[0]] + item[1]

	for d in dict3:               #calculate STDDEV
		a = float(dict3[d]) / float(dict2[d])
		dict3[d] = math.sqrt(a)

	return dict1 , dict3


def estimate(signalStrength):  #estimate d according to rssi and n values
	A = -26
	n = 3
	power = float(A - signalStrength)/float(10 * n)
	#print power
	d = math.pow(10, power)
	#print d
	return d


def calculate_distance(RSSI):
	distances = {}
	for ap in RSSI:
		distance = estimate(RSSI[ap])
		distances[ap] = distance

	return distances


def Draw(distances):
	fig = plt.figure(figsize=(20, 20))
	ax = plt.subplot(111, projection='polar')
	trans_offset = mtransforms.offset_copy(ax.transData, fig=fig,
                                       x=0.15, y=0.15, units='inches')

	for d in distances:
		m = randint(0,360)
		radin = m*math.pi/180
		print d, radin, distances[d]
		plt.polar(radin, distances[d], 'ro')
		plt.text(radin, distances[d], '%s, %.3f' %(str(d), float(distances[d])),
             transform=trans_offset,
             horizontalalignment='center',
             verticalalignment='bottom')

	plt.show()


def main():
	List = parser()
	RSSI , STDDEV = calc(List)
	draw(RSSI ,STDDEV)
	print RSSI
	distances = calculate_distance(RSSI)
	#print distances
	Draw(distances)


main()