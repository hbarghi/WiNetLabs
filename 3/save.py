## this script should be ran in each point 
## the output is a text file in this form
## x , y , rssi
## 1.create a text file named logRssi
## 2.run the iwconfig wlp2s0 | grep "Signal"
## 3.get the value of rssi 100 times and calculates the average value 
## 4.get the x and y from user
## 5.write the x , y and rssi in the logRssi.txt
import subprocess
from subprocess import PIPE , Popen
import csv
import os

def make_log_csv(coordinate, rssi):
	flag = False
	if os.path.isfile("logRssi.csv"):
		flag = True

	with open ("logRssi.csv" , "a+") as file:
		textwriter = csv.writer(file)
		if flag == False:
			textwriter.writerow(['xCol','yRow','Rssi'])	
		textwriter.writerow([coordinate[0] , coordinate[1] , rssi])
	

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


def getPoint():
	x = input("what is x coordinate?")
	y = input("what is y coordinate?")
	coordinate = [x , y]
	return coordinate


def get_avg():
	sum_rssi = 0
	for i in range(0 ,100):
		proc = Popen(['iwconfig' , 'wlp2s0'] , stdout=PIPE, shell=True)
		result = proc.stdout.read()	
		RSSI = getRssi(result)
		sum_rssi += RSSI
	avg = sum_rssi/100
	return avg


def main():
	COORDINATE = getPoint()
	avg = get_avg()
	make_log_csv(COORDINATE , avg)


if __name__ == "__main__":
	main()