import zgui.guilocal as local
from .slot import *
from .exception import *

class Signal:
	"""Signal Class for event handling"""

	def __init__(self,*args):
		self.argtype = args
		self.slots = []

	def __call__(self,*args):
		"""when call this signal"""
		if not self.slots: return
		'''
		for i in range(len(self.argtype)):
			try:
				self.argtype[i](args[i])
			except:
				GuiError("Signal call with wrong arguments type")
		'''
		for slot in self.slots:
			slot(*args)

	def connect(self,*args):
		self.slots.append(args[0])

	def disconnect(self,*args):
		self.slots[:] = [i for i in self.slots if not i==args[0]]

	def connectSlot(self,slot):
		self.slots.append(slot)

	def disconnectSlot(self,slot):
		self.slots[:] = [i for i  in self.slots if not i==slot]

class XSignal:
	"""Signal Class for event handling"""

	def __init__(self,*args):
		self.argtype = args
		self.slots = []

	def __call__(self,*args):
		"""when call this signal"""
		if not self.slots: return
		'''
		for i in range(len(self.argtype)):
			try:
				self.argtype[i](args[i])
			except:
				GuiError("Signal call with wrong arguments type")
		'''
		for slot in self.slots:
			slot(args)

	def connect(self,*args):
		slot = Slot(*args)
		self.slots.append(slot)

	def connectSlot(self,slot):
		self.slots.append(slot)

	def disconnectSlot(self,slot):
		self.slots[:] = [i for i  in self.slots if not i==slot]



class OldSignal:
	"""Old Signal """

	def __init__(self,*args):
		self.argtype = args
		self.slots = {}

	def __call__(self,*args):
		"""when call signal"""
		for i in range(len(self.argtype)):
			try:
				self.argtype[i](args[i])
			except:
				GuiError("Signal call with wrong arguments type")
		if self in local.signals:
			for slot in local.signals[self]:
				slot(args)

	def connect(self,*args):
		if not self in local.signals:
			local.signals[self] = []
		local.signals[self].append(Slot(*args))

	def disconnect(self,*args):
		if not self in local.signals:
			return
		for slot in local.signals[self]:
			if slot.func == args[0]:
				local.signals[self].remove(slot)




