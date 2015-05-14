import zgui.guilocal as local
from .base import *

class Layout(GUIObject):
	"""Layout Class for adjusting space"""

	def __init__(self,**args):
		super().__init__(**args)

		default = {}
		default['objects'] = []
		default['needreset'] = True
		default['margintop'] = 10
		default['marginleft'] = 10
		default['marginright'] = 10
		default['marginbot'] = 10
		default['spacing'] = 5
		default['sizehint'] = [10,10]
		default['sublayout'] = False
		self.setDefault(default,args)

	def __getitem__(self,key):
		"""get item like list"""
		if isinstance(key,int) and key < len(self['objects']) and key >=0:
			return self['objects'][key]
		else: return super().__getitem__(key)

	def __setitem__(self,key,val):
		"""set item like list"""
		if isinstance(key,int) and key < len(self['objects']) and key >=0:
			return self.change(key,val)
		else: return super().__setitem__(key,val)

	def change(self,idx,obj):
		"""change a item """
		self['objects'][idx] = obj
		self['needreset'] = True

		if isinstance(obj,Layout):
			obj.toSubLayout()


	def resize(self,size):
		self['size'] = size
		self['needreset'] = True

	def add(self,obj):
		"""add a item"""
		self['objects'].append(obj)
		self['needreset'] = True

		if isinstance(obj,Layout):
			obj.toSubLayout()

	def reset(self):
		return 

	def update(self):
		if self['needreset']: 
			self.reset()
			self['needreset'] = False

		for obj in self['objects']:
			obj.update()
		return

	def draw(self,screen):
		#surf = screen.subsurface(pygame.Rect(self['pos'],self['size'])) #self['background'].copy()

		for i in self['objects']:
			i.draw(screen)
		
		#screen.blit(surf,self['pos'])

	def toSubLayout(self):
		"""set self as sub layout"""
		self['sublayout'] = True
		self['margintop'] = 0
		self['marginleft'] = 0
		self['marginright'] = 0
		self['marginbot'] = 0

	def _update(self,pos,fks):

		self['onfocus'] = fks

		newp = pos[0]+self['pos'][0],pos[1]+self['pos'][1]
		self['screenpos'] = newp
		self['rect'] = pygame.Rect(newp,self['size'])
		
		if 'objects' in self.args:
			for obj in self['objects']:
				obj._update(pos,fks)

		self.basicEvent()

class BoxLayout(Layout):
	"""BoxLayout"""

	def __init__(self,**args):
		super().__init__(**args)


class HBoxLayout(BoxLayout):
	"""Horizontal Box Layout"""

	def __init__(self,**args):
		super().__init__(**args)


	def reset(self):
		if not self['objects']: return 

		n = len(self['objects'])
		x = begx = self['marginleft']
		y = begy = self['margintop']
		endx = self['size'][0]-self['marginright']
		endy = self['size'][1]-self['marginbot']
		totalspacing = (n-1)*self['spacing']

		totalheight = endy-begy
		totalwidth = endx-begx-totalspacing
		objtotalwidth = sum([ i['sizehint'][0] for i in self['objects']] )
		sizehintratio = totalwidth/objtotalwidth

		#self['sizehint'][0] = sum([ i['sizehint'][0] for i in self['objects']] )
		#self['sizehint'][1] = max([ i['sizehint'][1] for i in self['objects']] )

		for obj in self['objects']:
			obj['pos'] = pos_plus((int(x)-1,int(y)-1),self['pos'])
			size = (obj['sizehint'][0]*sizehintratio,totalheight)
			intsize = int(size[0]),int(size[1])
			if hasattr(obj,'resize'):obj.resize(intsize)
			else:obj['size'] = intsize
			x+=size[0]+self['spacing']

			if isinstance(obj,Layout):
				obj.reset()

class VBoxLayout(BoxLayout):
	"""Vertical Box Layout"""

	def __init__(self,**args):
		super().__init__(**args)

	def reset(self):
		if not self['objects']: return 

		n = len(self['objects'])
		x = begx = self['marginleft']
		y = begy = self['margintop']
		endx = self['size'][0]-self['marginright']
		endy = self['size'][1]-self['marginbot']
		totalspacing = (n-1)*self['spacing']

		totalheight = endy-begy-totalspacing
		totalwidth = endx-begx
		objtotalheight = sum([ i['sizehint'][1] for i in self['objects']] )
		sizehintratio = totalheight/objtotalheight

		#self['sizehint'][0] = max([ i['sizehint'][0] for i in self['objects']] )
		#self['sizehint'][1] = sum([ i['sizehint'][1] for i in self['objects']] )

		for obj in self['objects']:
			obj['pos'] = pos_plus((int(x),int(y)),self['pos'])
			size = totalwidth,obj['sizehint'][1]*sizehintratio

			intsize = int(size[0]),int(size[1])
			if hasattr(obj,'resize'):obj.resize(intsize)
			else:obj['size'] = intsize
			y+=size[1]+self['spacing']
			if isinstance(obj,Layout):
				obj.reset()



class FlowLayout(Layout):
	"""Flow Layout"""

	def __init__(self,**args):
		super().__init__(**args)


	def reset(self):
		if not self['objects']: return 

		n = len(self['objects'])
		x = begx = self['marginleft']
		y = begy = self['margintop']
		endx = self['size'][0]-self['marginright']
		endy = self['size'][1]-self['marginbot']

		#self['sizehint'][0] = sum([ i['sizehint'][0] for i in self['objects']] )
		#self['sizehint'][1] = max([ i['sizehint'][1] for i in self['objects']] )

		for obj in self['objects']:
			obj['pos'] = pos_plus((int(x),int(y)),self['pos'])
			x+=obj['size'][0]+self['spacing']

			if isinstance(obj,Layout):
				obj.reset()


class GridLayout(Layout):
	"""Grid Layout"""

	def __init__(self,**args):
		super().__init__(**args)

		grid = args['grid']
		self['row'] = grid[0]
		self['col'] = grid[1]
		self['objects'] = [ GUIObject() for i in range(self['col'] * self['row']) ]

	def reset(self):
		if not self['objects']: return 

		x = begx = self['marginleft']
		y = begy = self['margintop']
		endx = self['size'][0]-self['marginright']
		endy = self['size'][1]-self['marginbot']

		totx = endx-begx
		toty = endy-begy
		xlen = (totx-(self['col']-1)*self['spacing'])/self['col']
		ylen = (toty-(self['row']-1)*self['spacing'])/self['row']

		size = int(xlen),int(ylen)


		for i in range(len(self['objects'])):
			obj = self['objects'][i]
			obj['pos'] = pos_plus((int(x),int(y)),self['pos'])
			if hasattr(obj,'resize'):obj.resize(size)
			else: obj['size'] = size
			
			x+=size[0]+self['spacing']
			if (i+1)%self['col'] == 0:
				x = begx
				y+=size[1]+self['spacing']

			if isinstance(obj,Layout):
				obj.reset()

	def add(self,obj,pos):
		"""add to grid layout """

		p = pos[0]*self['col']+pos[1]
		self['objects'][p] = obj
		self['needreset'] = True

		if isinstance(obj,Layout):
			obj.toSubLayout()

	def change(self,pos,obj):
		"""change """
		self.add(obj,pos)


class StaticLayout(Layout):
	"""static Layout not finish"""

	pass