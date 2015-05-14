import zgui.guilocal as local
import os
import time,datetime

class Logger:
	"""Logger for log info"""
	def __init__(self,name):
		if not local.DEBUG: return
		self.file = open(name+'.log','w')
		self.time = time.asctime()
		self.log(self.time)

	def log(self,*args,end = os.linesep,prefix = ""):
		"""log"""
		if not local.DEBUG: return
		s = prefix
		for i in args:
			s+= str(i) + ' '
		s = s[:-1]
		print (s,end = end)
		self.file.write(s+end)
		self.file.flush()

	def info(self,*args,end = os.linesep):
		"""log info"""
		if not local.DEBUG: return
		s = "info: "
		for i in args:
			s+= str(i) + ' '
		s = s[:-1]
		print (s,end = end)
		self.file.write(s+end)
		self.file.flush()

	def error(self,*args,end = os.linesep):
		"""log error"""
		if not local.DEBUG: return
		s = "error: "
		for i in args:
			s+= str(i) + ' '
		s = s[:-1]
		print (s,end = end)
		self.file.write(s+end)
		self.file.flush()

	def warning(self,*args,end = os.linesep):
		"""log warning"""
		if not local.DEBUG: return
		s = "warning: "
		for i in args:
			s+= str(i) + ' '
		s = s[:-1]
		print (s,end = end)
		self.file.write(s+end)
		self.file.flush()