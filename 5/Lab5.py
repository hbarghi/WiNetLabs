import numpy as np
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
from subprocess import PIPE , Popen


scale = 50
Xrange = 0
Yrange = 0
matrix = np.zeros((Yrange,Xrange))
accesspoint = [20, 25]
accessPoint = [0,0]
PT = -13.7
PL_d0 = 20.3
Pd0 = [0,1]
D0 = 1
z = 1.65


def make_circle(r):
    t = np.arange(0, np.pi * 2.0, 0.01)
    t = t.reshape((len(t), 1))
    x = r * np.cos(t)
    y = r * np.sin(t)
    return np.hstack((x, y))


def setup():
	xx = input("please enter the map length : ")
	yy = input("please enter the map width : ")
	global Xrange,Yrange,matrix
	Xrange = xx * scale
	Yrange = yy * scale
	matrix.resize(Yrange,Xrange)


def Scale(x):
	return x*scale


def drawRing(r1 , r2 , ax):
	Path = mpath.Path
	inside_vertices = make_circle(r1)
	outside_vertices = make_circle(r2)
	codes = np.ones(
    	len(inside_vertices), dtype=mpath.Path.code_type) * mpath.Path.LINETO

	codes[0] = mpath.Path.MOVETO
	vertices = np.concatenate((outside_vertices[::-1],
                               inside_vertices[::1]))
	vertices[:, 0] += accesspoint[0]
	vertices[:, 1] += accesspoint[1]
	all_codes = np.concatenate((codes, codes))
	path = mpath.Path(vertices, all_codes)
	patch = mpatches.PathPatch(path, facecolor='blue', edgecolor='black', alpha = 0.4)
	ax.add_patch(patch)
	return ax


def getRssi(stdOut):
	splitted = stdOut.split("\n")
	answer = ""
	for line in splitted:
		if "Signal" in line :
			answer = line
	sig = answer.split("=")
	if len(sig) == 3 :
		num = sig[2].split(" ")
		return int(num[0])


def get_avg():
	sum_rssi = 0
	for i in range(0 ,100):
		proc = Popen(['iwconfig' , 'wlp2s0'] , stdout=PIPE, shell=True)
		result = proc.stdout.read()	
		RSSI = getRssi(result)
		sum_rssi += RSSI
	avg = sum_rssi/100
	return avg


def estimateLocation(rssi , n , sigma):
	exponential1 = (rssi - PT + PL_d0 - (z*sigma))/((-10)*n)
	exponential2 = (rssi - PT + PL_d0 + (z*sigma))/((-10)*n)
	d1 = (10**exponential1)*D0
	d2 = (10**exponential2)*D0
	return d1 , d2


def main():
	setup()
	fig, ax = plt.subplots()
	img = mpimg.imread('home.png')
	im1 = plt.imshow(img , extent=[0,Xrange,0,Yrange])
	RSSI = get_avg()
	r1, r2 = estimateLocation(RSSI , 2.4 , 0.8)
	print r1 , r2
	ax = drawRing(Scale(r1) , Scale(r2) , ax)
	plt.show()



if __name__ == "__main__":
	main()
