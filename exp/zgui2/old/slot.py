import zgui.guilocal as local
from .signal import *
from .exception import *

class Slot:
	"""Slot Class for Signal"""

	def __init__(self,func,*args):
		self.func = func
		self.argtype = args

	def __call__(self,*args):
		"""when call this slot"""
		'''
		for i in range(len(self.argtype)):
			try:
				self.argtype[i](args[i])
			except:
				GuiError("Slot call with wrong arguments type")
		'''
		self.func(*args)

