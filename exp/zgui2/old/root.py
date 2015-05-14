import zgui.guilocal as local
import pygame
from .base import *
from .guilocal import *
from .event import *
from .signal import *

class MainWindow(GUIObject):
	"""MainWindow, root of gui"""


	def __init__(self,**args):
		super().__init__(**args)

		default = {}
		default['objects'] = []
		default['onfocus'] = True
		default['pausefor'] = None
		default['pos'] = (0,0)
		default['rect'] = pygame.Rect((0,0),local.size)
		default['screenpos'] = (0,0)
		default['screen'] = None
		self.setDefault(default,args)

		self.Quit = Signal()
		self.menuBar = GUIObject()
		self.statusBar = GUIObject()

		self.lastp = None

	def update(self,evts):
		for e in evts:
			if e.type == QUIT:
				self.Quit()
		local.event = evts
		local.mouse.update()
		local.keyboard.update()
		local.size = pygame.display.get_surface().get_size()

		self.menuBar.update()
		self.statusBar.update()




		if self['pausefor']:
			self['pausefor'].update()
		else:
			for obj in reversed(self['objects']):
				if obj['visible']:
					obj.update()

		self._update()
		
		#self.debugOutput()
		

	def _update(self):

		self.basicEvent()

		if self['pausefor']:
			self['pausefor']._update((0,0),self['pausefor']['onfocus'])

		else:
			self.menuBar._update((0,0),False)
			self.statusBar._update((0,0),False)
			for i in reversed(self['objects']):
				if i['visible']:
					i._update((0,0),i['onfocus'])	

			

	def draw(self,screen):

		if not self['screen']: 
			if isinstance(screen, ExSurface):
				self['screen'] = screen
			else: self['screen'] = ExSurface(screen)

		for obj in self['objects']:
			if obj['visible']:
				obj.draw(self['screen'])

		self.menuBar.draw(self['screen'])
		self.statusBar.draw(self['screen'])

		if self['pausefor']:
			ps = ExSurface(self['size'])
			ps.fill(GRAY)
			ps.set_alpha(200)
			self['screen'].blit(ps,(0,0))
			self['pausefor'].draw(self['screen'])

	def add(self,obj,pos,priority = 0):
		"""add object to gui"""
		obj['pos'] = pos
		#if priority: self['objects'].append(obj)
		#else: self['objects'].insert(0,obj)
		self['objects'].append(obj)

		for i in reversed(range(len(self['objects']))):
			if isinstance(self['objects'][i], Window):
				self.changeFocus(self['objects'][i])
				break

	def remove(self,obj):
		"""remove object from gui"""
		self['objects'].remove(obj)

	def pauseFor(self,obj):
		"""pause gui for a object"""
		if self['pausefor']:
			self.lastp = self['pausefor']
		self['pausefor'] = obj

	def unpauseFor(self,obj):
		"""unpause for a object"""
		if self.lastp:
			self['pausefor'] = self.lastp
			self.lastp = None
		else:
			self['pausefor'] = None

	def changeFocus(self,obj):
		"""change current focus"""

		for i in reversed(range(len(self['objects']))):
			if 'onfocus' in self['objects'][i].args:
				if self['objects'][i]['onfocus'] == True:
					self['objects'][i].loseFocus()

		i = self['objects'].index(obj)	
		self['objects'][i].getFocus()

		tmp = self['objects'][i]
		self['objects'].remove(obj)
		self['objects'].append(tmp)	


	def debugOutput(self):
		"""output all user event for debugging"""
		inp = local.keyboard.getInput()
		if inp: print (inp)
		clk = local.mouse.down
		if clk!=[0,0,0] : print ('down',clk)
		u = local.mouse.up
		if u!=[0,0,0]: print('up',u)
		if local.mouse.wheel:
			print (local.mouse.wheel)

	def setMenuBar(self,menu):
		"""set menubar"""
		self.menuBar = menu	

	def setStatusBar(self,s):
		"""set statusbar"""
		self.statusBar = s




	
