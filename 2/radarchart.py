import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import math
from matplotlib.transforms import offset_copy
from random import randint



def draw(distances):
	fig = plt.figure(figsize=(20, 20))
	ax = plt.subplot(111, projection='polar')
	trans_offset = mtransforms.offset_copy(ax.transData, fig=fig,
                                       x=0.15, y=0.15, units='inches')


	for d in distances:
		m = randint(0,360)
		radin = m*math.pi/180
		print d, radin, distances[d]
		plt.polar(radin, distances[d], 'ro')
		plt.text(radin, distances[d], '%s, %d' %(str(d), int(distances[d])),
             transform=trans_offset,
             horizontalalignment='center',
             verticalalignment='bottom')

	plt.show()


distances = {'a': 8 ,'b': 32 ,'c': 72 ,'d': 50 ,'e': 20}
draw(distances)

