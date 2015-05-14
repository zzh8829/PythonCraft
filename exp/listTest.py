import time
import random
import numpy as np

import OpenGL
from OpenGL.GL import *

		
n = 9999999

class A:

	def __init__(self):
		self.a = None
	def b(self):
		self.a = np.empty(n)


a = A()
for i in range(10000):
	t1 = time.time()
	a.b()
	if i%100 == 0:
		print (time.time()-t1)