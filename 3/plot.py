import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import pandas as pd

scale = 50
Xrange = 0
Yrange = 0
dotSize = 10
datafile = pd.read_csv("logRssi.csv")
matrix = np.zeros((Yrange,Xrange))


def drawDot(y, x, index):
	y = abs(y - Yrange)	
	for i in range(-dotSize,dotSize):
		for j in range(-dotSize,dotSize):
			if y+i in range(0,Yrange) and x+j in range(0,Xrange):
				matrix[y+i][x+j] = datafile['Rssi'][index]


def setup():
	xx = input("please enter the map length : ")
	yy = input("please enter the map width : ")
	global Xrange,Yrange,matrix
	Xrange = xx * scale
	Yrange = yy * scale
	matrix.resize(Yrange,Xrange)

def main():
	setup()
	for i in range(len(datafile)):
		coordinateY = datafile['yRow'][i]*scale
		coordinateX = datafile['xCol'][i]*scale
		drawDot(coordinateY , coordinateX , i) 
    
	img = mpimg.imread('home.png')
		
	im1 = plt.imshow(img , extent=[0,Xrange,0,Yrange])

	im2 = plt.imshow(matrix, cmap=plt.cm.viridis, alpha=.4, interpolation='bilinear', extent=[0,Xrange,0,Yrange])

	for i in range(len(datafile)):
		coordinateY = datafile['yRow'][i]*scale
		coordinateX = datafile['xCol'][i]*scale
		text = plt.text(coordinateX, coordinateY, datafile['Rssi'][i], alpha = .4)  
    
	plt.show()


if __name__ == "__main__":
	main()