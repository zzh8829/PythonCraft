import pygame
import zgui2.render

# 0 -- 1
# |
# 1

class Signal:

	def __init__(self):
		self.func = []

	def connect(self,func):
		self.func.append(func)

	def disconnect(self,func):
		self.func.remove(func)

	def __call__(self,*args):
		for f in self.func:
			f(*args)

class GUIObject:

	def __init__(self):
		
		self.

