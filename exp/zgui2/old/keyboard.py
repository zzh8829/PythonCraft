import zgui.guilocal as local
import pygame
from .event import *

hahaha = [ 0 for i in range(512)]

class Keyboard:
	"""Custom Keyboard Class for event handling"""

	def __init__(self):

		self.keydown = hahaha[:]

		self.keyup = hahaha[:]

		self.pressed = hahaha[:]

		self.input = []

	def update(self):

		self.input = []
		self.keydown = hahaha[:]
		self.keyup = hahaha[:]

		for e in local.event:
			if e.type == KEYDOWN:
				self.keydown[e.key] = 1
				self.input.append(e)

			if e.type == KEYUP:
				self.keyup[e.key] = 1

		self.press = pygame.key.get_pressed()

	def clearInput(self):
		"""Clear input buffer"""
		self.input = []

	def getInput(self):
		"""Get Input Buffer"""
		inp =  self.input[:]
		return inp

	def getString(self):
		"""Get string of input buffer"""
		s = "".join(self.getInput())
		return s