import zgui.guilocal as local
import pygame
from .event import *

class Mouse:
	"""Custom Mouse Class for event handling"""

	def __init__(self):

		self.down = [0,0,0]
		self.up = [0,0,0]
		self.wheel = 0
		self.pos = [0,0]
		self.press = [0,0,0]

	def update(self):

		self.down = [0,0,0]
		self.up = [0,0,0]
		self.wheel = 0

		for e in local.event:
			if e.type == MOUSEBUTTONDOWN:
				if e.button < 4:
					self.down [e.button-1] = 1
			elif e.type == MOUSEBUTTONUP:
				if e.button == 4:
					self.wheel = 1
				elif e.button == 5:
					self.wheel = -1
				else:
					self.up [e.button-1] = 1

		self.pos = pygame.mouse.get_pos()
		self.press = list(pygame.mouse.get_pressed())

	def setCursor(self,cursor):
		"""set cursor to a image"""
		pygame.mouse.set_cursor(cursor)

	def setVisible(self,vis):
		"""set visibility of mouse cursor"""
		pygame.mouse.set_visible(vis)

	def setPos(self,pos):
		"""set position of mouse"""
		pygame.mouse.set_pos(pos)

	def getClick(self):
		"""get clicked button"""
		return self.down


