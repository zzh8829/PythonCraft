import zgui.guilocal as local
import pygame
import os
from .surface import *

class ResourceManager:
	"""resource Manager to save mamory"""

	def __init__(self,path = os.path.dirname(local.__file__)):
		self.res = {}
		self.folder = path

	def LoadImage(self,name):
		"""load image"""
		if ":" in name: path = name
		else: path = self.folder+'/'+name
		if not path in self.res: 
			try:
				self.res[path] = ExSurface(pygame.image.load(path))
			except:
				raise "Can't load Image"
		return self.res[path]

	def LoadFont(self,name,size):
		if not (name,size) in self.res:
			if name.endswith('.ttf'):
				path = self.folder+'/'+ name
				self.res[(name,size)] = pygame.font.Font(path,size)
			else:
				self.res[(name,size)] = pygame.font.SysFont(name,size)
		return self.res[(name,size)]
