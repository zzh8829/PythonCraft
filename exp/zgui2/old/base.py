import zgui.guilocal as local
import zgui
import pygame
import copy
from .guiglobal import *
from .color import *
from .surface import *
from .signal import *
from .utils import *
from .exception import *

class GUIObject:
	"""Abstract Base Class of all GUI Objects"""
	def __init__(self,**args):
		if not hasattr(self,'args'): self.args = {}
		self['pos'] = (0,0)
		self['screenpos'] = (0,0)
		self['size'] = (0,0)
		self['rect'] = pygame.Rect(0,0,0,0)
		self['sizehint'] = [10,10]
		self['needupdate'] = True
		self['onfocus'] = False
		self['visible'] = True
		self.mouseOver = Signal()
		self.mouseLeftUp = Signal()
		self.mouseRightUp = Signal()
		self.mouseMidUp = Signal()
		self.mouseLeftDown = Signal()
		self.mouseRightDown = Signal()
		self.mouseMidDown = Signal()
		self.mouseLeftPress = Signal()
		self.mouseRightPress = Signal()
		self.mouseWheelForward = Signal()
		self.mouseWheelBackward = Signal()
		self.keyDown = {}
		for i in range(512):
			self.keyDown[i] =  Signal()
		self.args.update(args)

	def __setitem__(self,key,val):
		"""implements dict to make access easiers"""
		self.args[key] = val

	def __getitem__(self,key):
		"""implements dict to make access easier"""
		return self.args[key]

	def __str__(self):
		"""implements str() function"""
		return '%s instance'%self.__class__.__name__

	def update(self):
		return

	def draw(self,screen):
		"""draw this object to surface"""
		return

	def setDefault(self,de,ar):
		"""set default arguments"""
		if not hasattr(self,'args'): self.args = {}
		for i in de:
			if not i in ar:
				self[i] = de[i]
				ar[i] = de[i]

	def copy(self):
		"""return deepcopy of this object"""
		return copy.deepcopy(self)

	def _update(self,pos,fks):
		self['onfocus'] = fks
		newp = pos[0]+self['pos'][0],pos[1]+self['pos'][1]
		self['screenpos'] = newp
		self['rect'] = pygame.Rect(newp,self['size'])
		
		if 'objects' in self.args:
			for obj in self['objects']:
				obj._update(newp,fks)
		if 'layout' in self.args:
			self['layout']._update(newp,fks)
		self.basicEvent()
		

	def basicEvent(self):
		"""basci events include mouse click"""
		#if not self['onfocus']: return
		if 'noevent' in self.args: return
		if self['rect'].collidepoint(local.mouse.pos):
			self.mouseOver()
			if local.mouse.up[0]:
				self.mouseLeftUp()
			if local.mouse.up[1]:
				self.mouseMidUp()
			if local.mouse.up[2]:
				self.mouseRightUp()
			if local.mouse.down[0]:
				self.mouseLeftDown()
			if local.mouse.down[1]:
				self.mouseMidDown()
			if local.mouse.down[2]:
				self.mouseRightDown()
			if local.mouse.press[0]:
				self.mouseLeftPress()
			if local.mouse.press[2]:
				self.mouseRightPress()
		if local.mouse.wheel == 1:
			self.mouseWheelForward()
		if local.mouse.wheel == -1:
			self.mouseWheelBackward()
		#for i in range(len(local.keyboard.keydown)):
		#	if local.keyboard.keydown[i]==1:
		#		self.keyDown[i]()

	def getFocus(self):
		"""if object get focus"""
		return

	def loseFocus(self):
		"""if object lose focus"""
		return

class Label2(GUIObject):
	"""Old label class"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['fontname'] = 'Arial'
		default['fontsize'] = 100
		default['text'] = 'label'
		default['textcolor'] = BLACK
		default['surface'] = None
		default['antialias'] = True
		self.setDefault(default,args)
		self['font'] = pygame.font.SysFont(self['fontname'],self['fontsize'])
		self['surface'] = ExSurface(self['font'].render(
			self['text'],self['antialias'],self['textcolor']
			))
		tsize = self['surface'].get_size()
		if 'size' in args:
			self.resize(args['size'])
		elif 'height' in args:
			h = args['height']
			w = h/tsize[1]*tsize[0]
			self.resize((int(w),int(h)))
		else:
			self['size'] = tsize

	def setText(self,text):
		"""set text for label"""
		self['text'] = str(text)
		self['surface'] = ExSurface(self['font'].render(
			self['text'],self['antialias'],self['textcolor']
			))
		self.resize(self['size'])

	def update(self):
		return

	def resize(self,size):
		self['surface'] = ResizeImage(self['surface'],size)
		self['size'] = size

	def draw(self,screen):
		screen.blit(self['surface'],self['pos'])

class Label(GUIObject):
	"""Label Class, blit text to surface"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['fontname'] = 'Arial'
		default['fontsize'] = 12
		default['text'] = 'label'
		default['textcolor'] = BLACK
		default['surface'] = None
		default['antialias'] = True
		self.setDefault(default,args)
		
		self.reset()

	def reset(self):
		self['font'] = local.resMgr.LoadFont(local.theme['UIFONT'],self['fontsize'])
		self['surface'] = ExSurface(self['font'].render(
			str(self['text']),self['antialias'],self['textcolor']
			))
		self['size'] = self['surface'].get_size()
	
		self.resize(self['size'])

	def setText(self,text):
		"""set text to label"""
		self['text'] = text
		self.reset()
		
	def update(self):
		return

	def resize(self,size):	
		delta = pos_minus(size,self['size'])
		self['pos'] = pos_plus(self['pos'],(delta[0]//2,delta[1]//2))

	def draw(self,screen):
		screen.blit(self['surface'],self['pos'])

class TextArea(GUIObject):
	"""TextArea, automataccly adjust text size"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['fontname'] = 'Arial'
		default['fontsize'] = 15
		default['text'] = 'Here are lots of text'
		default['textcolor'] = BLACK
		default['surface'] = None
		default['antialias'] = True
		default['linespace'] = 1.5
		self.setDefault(default,args)
		self.resize((local.size[0],100))

	def update(self):
		return

	def reset(self):
		self.resize(self['size'])

	def setText(self,text):
		"""set text to this object"""
		self['text'] = str(text)
		self.reset()

	def resize(self,size):
		width = size[0]
		f = pygame.font.SysFont(self['fontname'],self['fontsize'])
		height = f.get_linesize()
		space = f.render(' ',self['antialias'],self['textcolor'])
		spacewidth = space.get_size()[0]
		texts = self['text'].split('\n')
		surface = ExSurface((size),pygame.SRCALPHA)
		surfy = 0
		for line in texts:
			curw = 0
			words = line.split(' ')
			for word in words:
				surf = f.render(word,self['antialias'],self['textcolor'])
				ww = surf.get_size()[0]
				if curw+ww > width:
					curw = 0
					surfy+= height*(self['linespace'])
				surface.blit(surf,(curw,surfy))
				curw += ww+spacewidth
			surfy+= height*(self['linespace'])
		self['surface'] = surface
		self['size'] = size

	def draw(self,screen):
		screen.blit(self['surface'],self['pos'])

class Image(GUIObject):
	"""Draw an Image to surface"""

	def __init__(self,**args):
		default = {}
		default['filename'] = ""
		self.setDefault(default,args)
		super().__init__(**args)
		if not 'surface' in args:
			try:
				self['surface'] = ExSurface(pygame.image.load(self['filename']))
			except:
				self['surface'] = ExSurface((512,512),BLACK)
				GuiWarning("Loading image failed")
		size = self['surface'].get_size()
		if 'size' in args: size = args['size']
		self.resize(size)
			

	def update(self):
		return

	def resize(self,size):
		self['surface'] = ResizeImage(self['surface'],size)
		self['size'] = size

	def draw(self,screen):
		screen.blit(self['surface'],self['pos'])

class Button2(GUIObject):
	"""Old Button class"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['text'] = 'button'
		default['textcolor'] = BLACK
		default['state'] = 'up'
		default['border'] = 0.1 # precentage
		default['fontsize'] = 30
		img = {}
		img['over'] = ExSurface((256,256),local.theme['BUTTONOVER'])
		img['down'] = ExSurface((256,256),local.theme['BUTTONDOWN'])
		img['up'] = ExSurface((256,256),local.theme['BUTTONUP'])
		default['images'] = img
		self.setDefault(default,args)
		self['label'] = Label(text = self['text'],fontsize = self['fontsize'],textcolor=self['textcolor'])
		size = self['label']['size'][0]/(1-self['border']*2),self['label']['size'][1]/(1-self['border']*2)
		
		if not 'size' in args:
			self.resize(size)
	
		def mo():
			self['state'] = 'over'
		
		def mp():
			self['state'] = 'down'
		self.mouseOver.connect(mo)
		self.mouseLeftPress.connect(mp)

	def resize(self,size):
		self['size'] = size
		left = int(size[0]*self['border'])
		top = int(size[1]*self['border'])
		x = int(size[0]*(1-self['border']*2))
		y = int(size[1]*(1-self['border']*2))
		self['label'].resize((x,y))
		self['label']['pos']= (left,top)
		for key in self['images']:
			self['images'][key] = ResizeImage(self['images'][key],size)

	def update(self):
		self['state'] = 'up'

	def draw(self,screen):
		surf = self['images'][self['state']].copy()
		self['label'].draw(surf)
		pygame.draw.rect(surf.surface,local.theme['BUTTON%sBORDER'%self['state'].upper()],surf.get_rect(),1)
		screen.blit(surf,self['pos']) 

	def connect(self,s):
		self.mouseLeftUp.connect(Slot(s))


class Button(GUIObject):
	"""A button, let user to click on it"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['text'] = 'button'
		default['textcolor'] = BLACK
		default['state'] = 'up'
		default['border'] = 0.1 # precentage
		default['fontsize'] = 25
		default['downborder'] = local.theme['BUTTONDOWNBORDER']
		default['upborder'] = local.theme['BUTTONUPBORDER']
		default['overborder'] = local.theme['BUTTONOVERBORDER']
		default['selectedborder'] = local.theme['BUTTONDOWNBORDER']
		img = {}
		img['over'] = ExSurface((256,256),local.theme['BUTTONOVER'])
		img['down'] = ExSurface((256,256),local.theme['BUTTONDOWN'])
		img['up'] = ExSurface((256,256),local.theme['BUTTONUP'])
		img['selected'] = ExSurface((256,256),local.theme['BUTTONDOWN'])
		default['images'] = img
		self.setDefault(default,args)

		self['label'] = Label(text = self['text'],fontsize = self['fontsize'],textcolor=self['textcolor'])
		size = self['label']['size'][0]/(1-self['border']*2),self['label']['size'][1]/(1-self['border']*2)
		
		for key in self['images']:
			self['images'][key] = ResizeImage(self['images'][key],size)

		self['size'] = size
	
		def mo():
			if self['state'] != 'selected':
				self['state'] = 'over'
		
		def mp():
			if self['state'] != 'selected':
				self['state'] = 'down'
		self.mouseOver.connect(mo)
		self.mouseLeftPress.connect(mp)

		f = local.resMgr.LoadFont(local.theme['UIFONT'],self['fontsize'])
		a = f.render("BUTTON",True,RED)

	def resize(self,size):
		delta = pos_minus(size,self['size'])
		self['pos'] = pos_plus(self['pos'],(delta[0]//3,delta[1]//2))
		self['size'] = pos_plus(self['size'],((size[0]-self['size'][0])//3,0))
		for key in self['images']:
			self['images'][key] = ResizeImage(self['images'][key],self['size'])
		self['label']['pos'] = (0,0)
		self['label'].resize(self['size'])

	def update(self):
		if self['state'] != 'selected':
			self['state'] = 'up'

	def draw(self,screen):
		surf = self['images'][self['state']].copy()
		self['label'].draw(surf)
		pygame.draw.rect(surf.surface,self['%sborder'%self['state']],pygame.Rect((0,0),self['size']),1)
		screen.blit(surf,self['pos']) 

	def connect(self,s):
		self.mouseLeftUp.connect(s)

class Rectangle(GUIObject):
	"""Draw a rectangle to surface"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['color'] = WHITE
		default['sizehint'] = [10,10]
		self.setDefault(default,args)
		self.resize(self['size'])

	def resize(self,size):
		self['size'] = size
		self['surface'] = ExSurface(self['size'])
		self['surface'].fill(self['color'])
		if 'bordercolor' in self.args:
			pygame.draw.rect(self['surface'].surface,self['bordercolor'],self['surface'].get_rect(),1)

	def recolor(self,col):
		"""set color of rectangle"""
		self['color'] = col
		self['surface'].fill(col)
		if 'bordercolor' in self.args:
			pygame.draw.rect(self['surface'].surface,self['bordercolor'],self['surface'].get_rect(),1)

	def draw(self,screen):
		screen.blit(self['surface'],self['pos'])

class ColorRect(Rectangle):
	"""a colorful rectangle, change color with mouse move"""

	def __init__(self,**args):
		super().__init__(**args)
	
		def mouseover():
				self['color'] = PINK
		
		def mousedown():
				self['color'] = RED
		self.mouseLeftPress.connect(mousedown)
		self.mouseOver.connect(mouseover)

	def update(self):
		self['color'] = WHITE
		self['surface'] = ExSurface(self['size'])
		self['surface'].fill(self['color'])

class CloseButton(GUIObject):
	"""close button at top right cornor of window"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['text'] = 'button'
		default['textcolor'] = WHITE
		default['state'] = 'up'
		default['border'] = 0.1 # precentage
		default['fontsize'] = 100
		default['onfocus'] = True
		default['x'] = local.resMgr.LoadImage('res/close.png')
		default['type'] = 'BIG'
		default['w'] = 45
		self.setDefault(default,args)

		if self['type'] == 'BIG': self['w'] = 45
		elif self['type'] == 'SMALL': self['w'] = 31
		img = {}
		img['over'] = ExSurface((self['w'],20),(224,67,67))
		img['down'] = ExSurface((self['w'],20),(153,61,61))
		img['up'] = ExSurface((self['w'],20),(199,80,80))
		img['nofocus'] = ExSurface((self['w'],20),(188,188,188))
		for i in img:
			if self['type'] == 'BIG':
				img[i].blit(default['x'],(18,7))
			elif self['type'] == 'SMALL':
				img[i].blit(default['x'],(12,7))
		self['images'] = img
		
	
		def mo():
			self['state'] = 'over'
		
		def mp():
			self['state'] = 'down'
			local.mouse.down[0] = 0

		self.mouseOver.connect(mo)
		self.mouseLeftPress.connect(mp)

		self['size'] = (46,22)

	def resize(self,size):
		return

	def update(self):
		if self['onfocus']:
			self['state'] = 'up'
		else:
			self['state'] = 'nofocus'

	def draw(self,screen):
		screen.blit(self['images'][self['state']],self['pos']) 

	def connect(self,s):
		self.mouseLeftUp.connect(Slot(s))

	def setPos(self,w):
		"""set position of button"""
		self['pos'] = (w-self['w']-7,1)

class Container(GUIObject):
	"""Container Class, Can handle multiply objects"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['size'] = 512,512
		default['layout'] = None
		default['minsize'] = (20,20)
		default['bgcolor'] = local.theme['DIALOGBACKGROUND']
		self.setDefault(default,args)
		self['background'] = ExSurface(default['size'],self['bgcolor'])	
		self.resize(self['size'])
		self.mouseLeftUp.connect(self.u)
		self.mouseLeftDown.connect(self.d)
		self.mouseLeftPress.connect(self.p)

	def update(self):
		self['layout'].update()

	def draw(self,screen):
		
		surf = self['background'].copy()
		for i in self['layout']['objects']:
			i.draw(surf)
		screen.blit(surf,self['pos'])

	def setLayout(self,layout):
		"""set layout of container"""
		self['layout'] = layout
		self['layout']['size'] = self['size']
		self['layout'].reset()
		

	def resize(self,size):
		size = ValidateSize(size,self['minsize'])
		self['size'] = size
		self['background'] = ResizeImage(self['background'],size)
		if not self['layout']: return
		self['layout'].resize(size)

	def add(self,obj):
		"""add object to container"""
		self['layout'].add(obj)

	def u(self):
		local.mouse.up[0] = 0

	def d(self):
		local.mouse.down[0] = 0

	def p(self):
		local.mouse.press[0] = 0

class Window(Container):
	"""Window Obejct, Child of Container"""

	def __init__(self,**args):
		default = {}
		default['title'] = 'window'
		default['titleheight'] = 31
		default['closesize'] = 'BIG'
		default['moveable'] = True
		default['resizeable'] = True
		default['visible'] = True
		default['titlecolor'] = local.theme['WINDOWTITLEACTIVE']
		default['onfocus'] = False
		default['closeable'] = False
		default['borderoutcolor'] = local.theme['WINDOWBORDEROUTACTIVE']
		default['borderincolor'] = local.theme['WINDOWBORDERINACTIVE']
		default['resizeout'] = pygame.Rect(0,0,0,0)
		default['resizein']= pygame.Rect(0,0,0,0)
		default['minsize'] = (100,100)
		self.setDefault(default,args)
		
		args['closebutton'] = CloseButton(type = args['closesize'])
		args['closebutton'].mouseLeftUp.connect(self.close)

		super().__init__(**args)
		

		self.reset()
		self.pos = (0,0)
		self.SmoveOnPress = Slot(self.moveOnPress)
		self.SmoveOnDown = Slot(self.moveOnDown)
		self.SmoveOnUp = Slot(self.moveOnUp)
		self.SresizeOnPress = Slot(self.resizeOnPress)
		self.SresizeOnDown = Slot(self.resizeOnDown)
		self.SresizeOnUp = Slot(self.resizeOnUp)
		self.resizeLeftDown = Signal()
		self.moveLeftDown = Signal()
		self.afterResize = Signal()

		

	def moveOnPress(self):
		newpos = local.mouse.pos
		if newpos != self.pos:
			relx = newpos[0]-self.pos[0]
			rely = newpos[1]-self.pos[1]
			self.move((self['pos'][0]+relx,self['pos'][1]+rely))
		self.pos = newpos

	def moveOnDown(self):
		self.pos = local.mouse.pos
		local.gui.mouseLeftUp.connectSlot(self.SmoveOnUp)
		local.gui.mouseLeftPress.connectSlot(self.SmoveOnPress)
		

	def moveOnUp(self):
		local.gui.mouseLeftUp.disconnectSlot(self.SmoveOnUp)
		local.gui.mouseLeftPress.disconnectSlot(self.SmoveOnPress)

	def resizeOnPress(self):
		newpos = local.mouse.pos
		if newpos != self.pos:
			relx = newpos[0]-self.pos[0]
			rely = newpos[1]-self.pos[1]
			self.resize((self['size'][0]+relx,self['size'][1]+rely))
		self.pos = newpos
		self.afterResize(self['size'])

	def resizeOnDown(self):
		self.pos = local.mouse.pos
		local.gui.mouseLeftUp.connectSlot(self.SresizeOnUp)
		local.gui.mouseLeftPress.connectSlot(self.SresizeOnPress)
		

	def resizeOnUp(self):
		local.gui.mouseLeftUp.disconnectSlot(self.SresizeOnUp)
		local.gui.mouseLeftPress.disconnectSlot(self.SresizeOnPress)

	def basicEvent(self):
		"""Basic Event override"""
		if local.mouse.down[0]:
			if not self['onfocus'] and self['rect'].collidepoint(local.mouse.pos):
				local.gui.changeFocus(self)
			if self['resizeout'].collidepoint(local.mouse.pos) and not self['resizein'].collidepoint(local.mouse.pos):
				self.resizeLeftDown()
			if self['moverect'].collidepoint(local.mouse.pos):
				self.moveLeftDown()
		super().basicEvent()

	def update(self):
		self['layout'].update()			


	def reset(self):
		if self['closeable']: self['closebutton'].setPos(self['size'][0])
		surf = ExSurface(self['size'],self['titlecolor'])
		self['titletext'] = Label(text = self['title'],fontsize = 15,textcolor = BLACK)
		self['titletext']['pos'] = ((self['size'][0]-self['titletext']['size'][0])//2,5)
		self['titletext'].draw(surf)
		rect = pygame.Rect((0,0),self['size'])
		pygame.draw.rect(surf.surface, self['borderoutcolor'],rect, 1)
		rect.inflate_ip(-16,-16)
		rect[1]+=23;rect[3]-=23
		pygame.draw.rect(surf.surface, self['borderincolor'],rect, 1)
		self['surface'] = surf
		

	def setLayout(self,layout):
		"""set layout override"""
		self['layout'] = layout
		self['layout']['pos'] =  8,self['titleheight']
		self['layout']['size'] = self['size'][0]-16,self['size'][1]-self['titleheight']-8
		self['layout'].reset()

	def move(self,pos):
		"""move to new place"""
		self['pos'] = pos


	def resize(self,size):
		size = ValidateSize(size,self['minsize'])
		self['size'] = size
		self.reset()
		if not self['layout']: return
		self['layout']['pos'] =  8,self['titleheight']
		self['layout']['size'] = self['size'][0]-16,self['size'][1]-self['titleheight']-8
		self['layout'].reset()
		

	def draw(self,screen):
		
		surf = self['surface'].copy()
		surf.blit(ExSurface(self['layout']['size'],self['bgcolor']),
			pos_minus(self['layout']['pos'],(1,1)))
		self['layout'].draw(surf)
		if self['closeable']: self['closebutton'].draw(surf)
		screen.blit(surf,self['pos'])

	def _update(self,pos,fks):
		self['onfocus'] = fks
		newp = pos[0]+self['pos'][0],pos[1]+self['pos'][1]
		self['moverect'] = pygame.Rect(newp,(self['size'][0],self['titleheight']))
		self['rect'] = pygame.Rect(newp,self['size'])
		self['resizeout'] = pygame.Rect(newp,self['size'])
		self['resizein'] = self['resizeout'].inflate(-16,-16)
		
		if 'objects' in self.args:
			for obj in self['objects']:
				obj._update(newp,fks)
		if 'layout' in self.args:
			self['layout']._update(newp,fks)

		if self['closeable']:
			self['closebutton']['onfocus'] = self['onfocus']
			self['closebutton'].update()
			self['closebutton']._update(newp,fks)

		self.basicEvent()
		

	def loseFocus(self):
		"""when lost focus"""
		self['onfocus'] = False
		self['borderoutcolor'] = local.theme['WINDOWBORDEROUTINACTIVE']
		self['borderincolor'] = local.theme['WINDOWBORDEROUTINACTIVE']
		self['titlecolor'] = local.theme['WINDOWTITLEINACTIVE']
		self.reset()
		if self['moveable']: self.moveLeftDown.disconnectSlot(self.SmoveOnDown)
		if self['resizeable']: self.resizeLeftDown.disconnectSlot(self.SresizeOnDown)

	def getFocus(self):
		"""when get focus"""
		self['onfocus'] = True
		self['titlecolor'] = local.theme['WINDOWTITLEACTIVE']
		self['borderoutcolor'] = local.theme['WINDOWBORDEROUTACTIVE']
		self['borderincolor'] =  local.theme['WINDOWBORDERINACTIVE']
		self.reset()
		if self['moveable']: self.moveLeftDown.connectSlot(self.SmoveOnDown)
		if self['resizeable']: self.resizeLeftDown.connectSlot(self.SresizeOnDown)

	def close(self):
		"""when close"""
		local.gui.remove(self)

class Dialog(Window):
	"""Dialog Object, chiled of Window"""

	def __init__(self,**args):
		args['bgcolor'] = local.theme['DIALOGBACKGROUND']
		args['closeable'] = True
		super().__init__(**args)
		self['resizeable'] = False
		pos = (local.size[0]-self['size'][0])//2 , (local.size[1]-self['size'][1])//2
		local.gui.add(self,pos)
		local.gui.pauseFor(self)

	def update(self):
		local.gui.changeFocus(self)
		self['layout'].update()

	def close(self):
		"""when close"""
		local.gui.remove(self)
		local.gui.unpauseFor(self)

class MessageBox(Dialog):
	"""MessageBox object, a dialog to display text"""

	def __init__(self,**args):
		if not 'size' in args:
			args['size'] = (300,200)
		if not 'ratio' in args:
			args['ratio'] = 0.5
		
		super().__init__(**args)
		default = {}
		default['text'] = 'message'
		default['title'] = 'Message Box'
		default['return'] = 'ok'
		self.setDefault(default,args)
		self.ok = Button(text = 'OK')
		self.ok.mouseLeftUp.connect(self.onOK)
		t = TextArea(text = self['text'],fontsize=18,linespace= 1.2)
		layout = zgui.layout.VBoxLayout()
		layout.add(t)
		t['sizehint'] = [10,10/self['ratio']]
		bl = zgui.layout.HBoxLayout()
		bl.add(GUIObject())
		bl.add(self.ok)

		layout.add(bl)
		self.setLayout(layout)

	def onOK(self):
		self['return'] = 'ok'
		self.close()

class YesNoBox(Dialog):
	"""MessageBox with 2 options"""

	def __init__(self,**args):
		args['size'] = (400,200)		
		super().__init__(**args)
		default = {}
		default['text'] = 'message'
		default['title'] = 'Message Box'
		default['return'] = 'ok'
		self.setDefault(default,args)
		self.yes = Button(text = 'Yes')
		self.yes.mouseLeftUp.connect(self.onYes)
		self.no = Button(text = 'No')
		self.no.mouseLeftUp.connect(self.onNo)
		t = TextArea(text = self['text'],fontsize=18,linespace= 1.2)
		layout = zgui.layout.VBoxLayout()
		layout.add(t)
		bl = zgui.layout.HBoxLayout()
		bl.add(self.yes)
		bl.add(self.no)
		layout.add(bl)
		self.setLayout(layout)

	def onYes(self):
		self['return'] = 'yes'
		self.close()

	def onNo(self):
		self['return'] = 'no'
		self.close()

class YesNoCancelBox(Dialog):
	"""MessageBox with 3 options"""

	def __init__(self,**args):
		args['size'] = (400,200)		
		super().__init__(**args)
		default = {}
		default['text'] = 'message'
		default['title'] = 'Message Box'
		default['return'] = 'ok'
		self.setDefault(default,args)
		self.yes  = Button(text = 'Yes')
		self.yes.mouseLeftUp.connect(self.onYes)
		self.no = Button(text = 'No')
		self.no.mouseLeftUp.connect(self.onNo)
		self.cancel = Button(text = 'Cancel')
		self.cancel.mouseLeftUp.connect(self.onCancel)
		t = TextArea(text = self['text'],fontsize=18,linespace= 1.2)
		t['sizehint'] = (10,20)
		layout = zgui.layout.VBoxLayout()
		layout.add(t)
		bl = zgui.layout.HBoxLayout()
		bl.add(self.yes)
		bl.add(self.no)
		bl.add(self.cancel)
		layout.add(bl)
		self.setLayout(layout)

	def onYes(self):
		self['return'] = 'yes'
		self.close()

	def onNo(self):
		self['return'] = 'no'
		self.close()

	def onCancel(self):
		self['return'] = 'cancel'
		self.close()

class Space(GUIObject):
	"""A Space to waste space"""

	def __init__(self,**args):
		super().__init__(**args)

	def update(slef):
		return

	def draw(self,screen):
		return

	def _update(self,focus):
		return

class MenuItem(GUIObject):
	"""MenuItem object"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['text'] = 'button'
		default['textcolor'] = BLACK
		default['state'] = 'up'
		default['border'] = 0.08 # precentage
		default['fontsize'] = 14
		img = {}
		img['over'] = ExSurface((256,256),local.theme['MENUDOWN'])
		img['down'] = ExSurface((256,256),local.theme['MENUDOWN'])
		img['up'] = ExSurface((256,256),local.theme['POPMENUBACKGROUND'])
		default['images'] = img
		self.setDefault(default,args)
		self['label'] = Label(text = self['text'],fontsize = self['fontsize'],textcolor=self['textcolor'])
		size = self['label']['size'][0]/(1-self['border']*2),self['label']['size'][1]/(1-self['border']*2)
		if not 'size' in args:
			self.resize(size)
		self['label'].reset()
		
		def mo():
				self['state'] = 'over'
		
		def mp():
				self['state'] = 'down'
		self.mouseOver.connect(mo)
		self.mouseLeftPress.connect(mp)

	def resize(self,size):
		self['size'] = size
		left = int(size[0]*self['border'])
		top = int(size[1]*self['border'])
		x = int(size[0]*(1-self['border']*2))
		y = int(size[1]*(1-self['border']*2))
		self['label'].resize((x,y))
		self['label']['pos']= (left,top)
 
		for key in self['images']:
			self['images'][key] = ResizeImage(self['images'][key],size)

	def update(self):
		self['state'] = 'up'

	def draw(self,screen):
		surf = self['images'][self['state']].copy()
		self['label'].draw(surf)
		if self['state']!= 'up':
			rect = pygame.Rect((0,0),self['size'])
			pygame.draw.rect(surf.surface,local.theme['BUTTONDOWNBORDER'],rect,1)
		screen.blit(surf,self['pos']) 

class Menu(Button):
	"""Menu object, has a popmenu inside"""

	def __init__(self,**args):
		args['textcolor'] = BLACK
		args['fontsize'] = 13
		args['downborder'] = local.theme['MENUDOWNBORDER']
		args['upborder'] = local.theme['MENUBAR']
		args['overborder'] = local.theme['MENUDOWNBORDER']
		super().__init__(**args)
		self['images']['down'].fill(local.theme['MENUDOWN'])
		self['images']['up'].fill(local.theme['MENUBAR'])
		self['images']['over'].fill(local.theme['MENUOVER'])
		self['width'] = 80
		self['win'] = Container(size = (80,20),bgcolor = local.theme['POPMENUBACKGROUND'])
		l = zgui.layout.VBoxLayout()
		l['margintop']=2
		l['marginbot']=2
		l['marginleft']=2
		l['marginright']=2
		l['spacing'] = 2
		self['win'].setLayout(l)
		self.mouseLeftUp.connect(self.onClick)
		self.SonUp = Slot(self.onUp)

		self.resize(pos_plus((self['size']),(8,0)))

	def onClick(self):
		local.gui.add(self['win'],(self['pos'][0],self['pos'][1]+21))
		local.gui.changeFocus(self['win'])
		local.gui.statusBar.setText(self['text']+' Menu')
		local.gui.mouseLeftUp.connectSlot(self.SonUp)

	def onUp(self):
		if self['win']['rect'].collidepoint(local.mouse.pos):
			for i in self['win']['layout']['objects']:
				if i['rect'].collidepoint(local.mouse.pos):
					i.mouseLeftUp()
			local.mouse.down[0]=0
			local.mouse.up[0]=0
			local.mouse.press[0]=0
		local.gui.remove(self['win'])
		local.gui.mouseLeftUp.disconnectSlot(self.SonUp)

	def add(self,obj):
		"""add MenuItem to popmenu"""
		self['win']['layout'].add(obj)
		self['width'] = max(self['width'],len(obj['text'])*9)
		self['win'].resize( (self['width'],25*len(self['win']['layout']['objects'] )) )

	def resize(self,size):
		self['size'] = size[0],size[1]-3
		for key in self['images']:
			self['images'][key] = ResizeImage(self['images'][key],self['size'])
		self['label']['pos'] = (0,0)
		self['label'].resize(self['size'])

class MenuBar(Container):
	"""container some menus"""

	def __init__(self,**args):
		args['bgcolor'] = local.theme['MENUBAR']
		super().__init__(**args)
		self['pos'] = 0,0
		self.resize((local.size[0],20))
		l = zgui.layout.FlowLayout()
		l['margintop']=0
		l['marginbot']=0
		l['marginleft']=0
		l['marginright']=2
		l['spacing'] = 0
		self.setLayout(l)	

	def draw(self,screen):
		
		surf = self['background'].copy()
		for i in self['layout']['objects']:
			i.draw(surf)
		screen.blit(surf,self['pos'])
		pygame.draw.line(screen.surface,local.theme['MENUBORDER'],(0,self['size'][1]),(self['size'][0],self['size'][1]))

	def add(self,menu):
		"""add menu to menubar"""
		self['layout'].add(menu)

class StatusBar(Container):
	"""status bar object"""

	def __init__(self,**args):
		args['pos'] = 0,local.size[1]-20
		args['size'] = local.size[0],20
		super().__init__(**args)
		l = zgui.layout.FlowLayout()
		l['margintop']=1
		l['marginbot']=1
		l['marginleft']=5
		l['marginright']=5
		l['spacing'] = 10
		self.setLayout(l)	
		self['textarea'] = TextArea(text = "",fontsize=16,linespace= 1.2,textcolor = BLACK)
		l.add(self['textarea'])

	def setText(self,text):
		"""set text of status bar"""
		self['textarea']['text'] = text
		self['textarea'].reset()

class Spacing(GUIObject):
	"""A space to waste space"""

	def __init__(self,**args):
		super().__init__(**args)
		self['noevent'] = 1

class TransRect(Rectangle):
	"""Draw a Transparent Rectangle, GUIObject"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['color'] = WHITE
		default['alpha'] = 100
		default['size'] = (100,100)
		self.setDefault(default,args)
		self['surface'] = ExSurface(self['size'])
		self['surface'].fill(self['color'])
		self['surface'].set_alpha(self['alpha'])

	def resize(self,size):
		self['size'] = size
		self['surface'] = ExSurface(self['size'])
		self['surface'].fill(self['color'])
		self['surface'].set_alpha(self['alpha'])

class Slider(GUIObject):
	"""Allow user to slide block and get value, GUIObject"""

	def __init__(self,**args):
		super().__init__(**args)
		default = {}
		default['bgcolor'] = BLACK
		default['range'] = (0,100)
		default['value'] = 0
		default['objects'] = []
		self.setDefault(default,args)
		self['block'] = TransRect(color = BLACK,alpha = 100)
		self['length'] = self['range'][1]-self['range'][0]
		self.reset()
		self.SslideDown= Slot(self.slideDown)
		self.SslidePress = Slot(self.slidePress)
		self.SslideUp = Slot(self.slideUp)
		self['block'].mouseLeftDown.connectSlot(self.SslideDown)
		self.valueChanged = Signal(int)

	def slideDown(self):
		local.gui.mouseLeftPress.connectSlot(self.SslidePress)
		local.gui.mouseLeftUp.connectSlot(self.SslideUp)
		self.oldpos = local.mouse.pos

	def slidePress(self):
		pos = local.mouse.pos
		shift = pos[0]-self.oldpos[0]
		pre = shift/self['size'][0]
		val = self['value']+self['length']*pre
		self.setValue(val)
		self.oldpos = pos
		self.resetBlock()

	def slideUp(self):
		local.gui.mouseLeftUp.disconnectSlot(self.SslideUp)
		local.gui.mouseLeftPress.disconnectSlot(self.SslidePress)

	def setValue(self,val):
		"""set value of slider"""
		if val<self['range'][0]:
			self['value'] = self['range'][0]
		elif val>self['range'][1]:
			self['value'] = self['range'][1]
		else:
			self['value'] = val
		self.valueChanged(self['value'])

	def reset(self):
		self['background'] = ExSurface((512,512),self['bgcolor'])
		self.resetBlock()

	def resize(self,size):
		self['size'] = size
		self['background'] = ResizeImage(self['background'],size)
		self.resetBlock()

	def resetBlock(self):
		pre = (self['value']-self['range'][0])/self['length']
		leng = self['size'][0]
		x = leng*pre+self['pos'][0]-7
		y = self['pos'][1]-7
		h = self['size'][1]+14
		w = 14
		self['block']['pos'] = x,y
		self['block'].resize((w,h))

	def draw(self,screen):
		screen.blit(self['background'],self['pos'])
		self['block'].draw(screen)

	def _update(self,pos,fks):
		self['onfocus'] = fks
		newp = pos[0]+self['pos'][0],pos[1]+self['pos'][1]
		self['screenpos'] = newp
		self['rect'] = pygame.Rect(newp,self['size'])
		self['block']._update(pos,fks)
		self.basicEvent()
