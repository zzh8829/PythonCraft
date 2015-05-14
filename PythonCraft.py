import OpenGL
import os
from math import *
#os.system("cpy.bat")
import main
level = main.CLevel('saves/','broville')
#level = main.CLevel('C:/Users/Zihao/AppData/Roaming/.minecraft/saves/','exmaple')
wd = level.getWorld()
render = main.CLevelRender(level)
render.getWorldRender().setViewDistance(16)

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import * 
from Camera import *
from Texture import *
from Skybox import * 

import Tessellator

import time

#SCREEN_SIZE = 854,480
SCREEN_SIZE = 1920,1080
SCREEN_FLAG = OPENGL|DOUBLEBUF|HWSURFACE|FULLSCREEN
pygame.init()
font = pygame.font.SysFont("Arial",15)
main.SetVsync(False)
pygame.display.set_mode(SCREEN_SIZE,SCREEN_FLAG)

RED = (1.0,0.0,0.0,1.0)
GREEN = (0.0,0.0,1.0,1.0)
BLUE= (0.0,1.0,0.0,1.0)
BLACK = (0.0,0.0,0.0,1.0)
WHITE = (1.0,1.0,1.0,1.0)

YP = 0
YM = 1
XP = 2
XM = 3
ZP = 4
ZM = 5

vertexbuffer = 0
indexbuffer = 0
vertices = [0,0,0, 1,0,0, 0,1,0, 1,1,0,	0,0,1, 1,0,1, 0,1,1, 1,1,1]
indices = [2,3,7,6, 4,5,1,0, 0,1,3,2, 1,5,7,3, 5,4,6,7, 4,0,2,6]
import os


DELTA = [(0,1,0),(0,-1,0),(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)]

def _floatToInt(n):
	return int(floor(n))

def floatToInt(*args):
	return tuple(map(_floatToInt,args))

class World:

	def __init__(self):

		self.emptyChunk = 123123123

		self.viewDistance = 1

		self.fpsCount = 0

		self.worldTime = 0
		self.worldHour = 0
		self.worldMinute = 0
		self.worldSecond = 0

		self.updateQueue = []

	def timeChange(self,delta):
		# delta real world second

		# 1s = 0.0008333333333333333 game day
		# 1s = 0.02 game hour
		# 1s = 1.2 game min
		# 1s = 72 game second

		self.worldTime += delta
		self.worldDay = (self.worldTime*0.0008333333333333333)%365
		self.worldHour = (self.worldTime*0.02)%24
		self.worldMinute = (self.worldTime*1.2)%60
		self.worldSecond = (self.worldTime*72)%60



	def getBlock(self,x,y,z):
		return wd.getBlockId(x,y,z)

	def setBlock(self,x,y,z,ID):
		wd.setBlockId(x,y,z,ID)

	def getRayHit(self,orgin,direction,length=100):
		for i in range(length):
			pos = orgin+i/10*direction
			#y = _floatToInt(pos.y)
			#ry = (pos.y-y)/direction.y
			#pos -= direction*ry
			x,y,z = floatToInt(*pos.toList())
			if self.getBlock(x,y,z) != 0:
				return floatToInt(*(pos-direction).toList()) + (x,y,z)
		return False


def genSelect():
	l = glGenLists(1)
	glNewList(l,GL_COMPILE)
	glDisable(GL_TEXTURE_2D)
	glColor3f(0,0,0)
	tes = Tessellator.instance
	tes.startDrawing(GL_LINE_STRIP)
	for i in range(6):
		v1 = indices[i*4]*3
		v2 = indices[i*4+1]*3
		v3 = indices[i*4+2]*3
		v4 = indices[i*4+3]*3
		tes.addVertex(vertices[v1],vertices[v1+1],vertices[v1+2])
		tes.addVertex(vertices[v2],vertices[v2+1],vertices[v2+2])
		tes.addVertex(vertices[v3],vertices[v3+1],vertices[v3+2])
		tes.addVertex(vertices[v4],vertices[v4+1],vertices[v4+2])
	tes.draw()
	glEnable(GL_TEXTURE_2D)
	glEndList()
	return l

selectBlock = genSelect()
world = World()

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

class GUIBase:

	def __init__(self,pos=(0,0),size = (0,0)):

		self.mouseClick = Signal()
		self.rect = pygame.Rect(0,0,0,0)

	def update(self,event):
		pass

	def render(self,surface):
		pass

class RandomRect(GUIBase):

	def __init__(self,pos=(0,0),size=(0,0)):
		super().__init__(pos,size)
		self.rect = pygame.Rect(pos,size)

	def update(self,event):
		pass

	def render(self,surface):
		pygame.draw.rect(surface,(0,0,0),(0,0,100,100))

class MainMenu(GUIBase):

	def __init__(self):
		super().__init__(size = SCREEN_SIZE)

		self.objs = {}

	def update(self,event):
		for obj in self.objs.items():
			obj.update(event)

	def render(self,screen):
		for obj in self.objs.items():
			obj.render(screen )



class GUI:

	def __init__(self):
		self.screen = pygame.Surface((SCREEN_SIZE[0],SCREEN_SIZE[1]),SRCALPHA)
		self.texture = None

		self.object = []

	def render(self):

		for i in self.object:
			i.render(self.screen)

		if self.texture:
			deleteTexture(self.texture)
		self.texture = createTexture(self.screen)
		renderTexture(self.texture[0],(0,0),(self.texture[1],self.texture[2]))

	def update(self,event):
		for i in self.object:
			i.update(event)

	def add(self,obj):
		self.object.append(obj)




class Game:
	def __init__(self):
		self.display_init()
		self.running = True
		self.clock = pygame.time.Clock()

		self.skybox = Skybox('textures/skybox/minecraft','png')
		self.camera = Camera()
		#print(level.playerX,level.playerY,level.playerZ)
		self.camera.setPosition((level.playerX,level.playerY,level.playerZ))
		#self.camera.setPosition(cn.level.playerPos)
		#self.camera.setPosition((0,70,0))

		self.plane = glGenLists(1)

		self.ID = 3

		glNewList(self.plane,GL_COMPILE)
		glPushMatrix()
		glColor3ub(66,66,66)
		tes = Tessellator.instance
		tes.startDrawing(GL_LINES)
		for i in range(-50,50):
			tes.addVertex(-50, 0, i)
			tes.addVertex(50, 0, i)
			tes.addVertex(i, 0,-50)
			tes.addVertex(i, 0, 50)
		tes.draw()
		glPopMatrix()
		glEndList()

		self.groundpos = None
		self.cubepos = Vector3()
		self.near = Vector3()
		self.far = Vector3()


		self.lasttime = time.time()

		self.cloudTickCounter = 0

		self.hit = None

		main.CTextureManager.initialize("textures")

		self.lastpos = Vector3(0,0,0)

		self.gui = GUI()

		self.gui.add(RandomRect())

	def run(self):
		while self.running:
			delta = time.time()-self.lasttime
			self.lasttime += delta

			world.timeChange(delta*10)

			self.event_handler(pygame.event.get())
			self.key_handler(pygame.key.get_pressed())
			self.mouse_handler(pygame.mouse.get_pressed())
			self.renderScene(delta)
			self.timer()
			pygame.display.flip()

		pygame.quit()

	def display_init(self):
		#self.screen = pygame.display.set_mode(SCREEN_SIZE,SCREEN_FLAG)
		glClearColor(*BLACK)
		glClearDepth(1)
		w = SCREEN_SIZE[0]
		h = SCREEN_SIZE[1]
		aspectRatio= w/h
		glViewport(0,0,w,h)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(35.0, w/h, 0.1 , 10000.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		pygame.mouse.set_visible(True)
		pygame.mouse.set_pos((w//2,h//2))

		#glEnable(GL_LIGHTING)
		#glLightfv(GL_LIGHT0, GL_AMBIENT,(0.95,0.95,0.95,1))
		#glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5,0.5,0.5,1.0))
		#glLightfv(GL_LIGHT0, GL_SPECULAR, (0.95,0.95,0.95,1.0))
		#glLightfv(GL_LIGHT0, GL_POSITION, (-1,1,1,0 ))
		#glEnable(GL_LIGHT0)

		#glEnable(GL_FOG)
		#glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
		#glHint(GL_FOG_HINT, GL_DONT_CARE)
		#glFogi(GL_FOG_MODE, GL_LINEAR)sz
		#glFogf(GL_FOG_DENSITY, 0.35)
		#glFogf(GL_FOG_START, 20.0)
		#glFogf(GL_FOG_END, 60.0)

		print(glGetString(GL_VERSION))

		glEnable( GL_ALPHA_TEST)
		glEnable (GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)

		#glMaterialfv(GL_FRONT, GL_SPECULAR, (1,1,1,1));
		#glMaterialfv(GL_FRONT, GL_SHININESS, (50.0));
		#glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);
		#glEnable(GL_COLOR_MATERIAL);

	def renderScene(self,delta):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		playerPos = self.camera.position.copy()
		playerPos.z = -playerPos.z

		self.camera.setPerspective()
		
	
		near,far = self.camera.getMouseRay(*pygame.mouse.get_pos())

		direction = far-near
		direction.normalise()

		position = Vector3(self.camera.position)
		position.z = -position.z

		self.groundpos = None

		self.hit = world.getRayHit(position,direction)
		if self.hit:
			self.groundpos = Vector3(self.hit[:3])
			self.delPos = Vector3(self.hit[3:6])


		# Instance of Tessellator
		qb = main.CQuadBuilder.getInstance()
		
		# Render Sky

		glDisable(GL_LIGHTING)
		self.skybox.render()

		# Render Sun
		glPushMatrix()
		glTranslatef(playerPos.x,playerPos.y,playerPos.z)
		glRotatef(-90.0, 1.0, 0.0, 0.0)
		glRotatef(7.5*world.worldHour,1.0,0.0,0.0)
		sunp = 30.0
		glColor4f(1.0, 1.0, 1.0, 1.0)
		glEnable(GL_TEXTURE_2D)
		glEnable(GL_BLEND)	
		glBlendFunc(GL_SRC_ALPHA, GL_ONE)	
		glBindTexture(GL_TEXTURE_2D,main.CTextureManager.getInstance().getTexture("sun").id)	
		qb.begin()
		qb.addVertexWithUV(-sunp, 300.0, -sunp, 0.0, 0.0)
		qb.addVertexWithUV(sunp, 300.0, -sunp, 1.0, 0.0)
		qb.addVertexWithUV(sunp, 300.0, sunp, 1.0, 1.0)
		qb.addVertexWithUV(-sunp, 300.0, sunp, 0.0, 1.0)
		qb.render()
		glDisable(GL_BLEND)
		glPopMatrix()

		# Render Clouds
		glPushMatrix()

		glTranslatef(playerPos.x,playerPos.y,playerPos.z)

		predictY = self.camera.position.y
		spacing = 32
		amount = int(256 / spacing)
		glBindTexture(GL_TEXTURE_2D,main.CTextureManager.getInstance().getTexture("clouds").id)	
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		red = 1.0
		green = 1.0
		blue = 1.0

		small = 4.8828125e-4
		cloudTick = (self.cloudTickCounter + delta)*500
		self.cloudTickCounter+= delta
		predictX = self.camera.position.x + cloudTick * 0.029999999329447746
		predictZ = -self.camera.position.z
		tx = floor(predictX/2048)
		tz = floor(predictZ/2048)
		predictX -= (tx * 2048)
		predictZ -= (tz * 2048)
		#y = 128 - predictY + 0.33
		y = 128
		cloudX = (predictX * small)
		cloudZ = (predictZ * small)
		qb.begin()

		for ix in range(-spacing*amount,spacing*amount,spacing):
			for iz in range(-spacing*amount,spacing*amount,spacing):
				qb.addColor(red, green, blue, 0.8)
				qb.addVertexWithUV((ix + 0), y, (iz + spacing), ((ix + 0) * small + cloudX), ((iz + spacing) * small + cloudZ))
				qb.addColor(red, green, blue, 0.8)
				qb.addVertexWithUV((ix + spacing), y, (iz + spacing), ((ix + spacing) * small + cloudX), ((iz + spacing) * small + cloudZ))
				qb.addColor(red, green, blue, 0.8)
				qb.addVertexWithUV((ix + spacing), y, (iz + 0), ((ix + spacing) * small + cloudX), ((iz + 0) * small + cloudZ))
				qb.addColor(red, green, blue, 0.8)
				qb.addVertexWithUV((ix + 0), y, (iz + 0), ((ix + 0) * small + cloudX), ((iz + 0) * small + cloudZ))
		qb.render()
		glDisable(GL_BLEND)
		glPopMatrix()
		

					
		# Render World
		self.renderworld(playerPos)

		
		glPushMatrix()
		if self.groundpos:
			glTranslatef(*floatToInt(*self.groundpos.toList()))
			glCallList(selectBlock)

		glPopMatrix()
		
		self.drawText()

		#self.gui.render()

	def renderworld(self,playerPos):
		if 1:
			vii = wd.getLoadedRegions()
			cr = playerPos.toList()
			for i in range(len(cr)):
				cr[i] = (int(floor(cr[i]))>>4 )>> 5
			for i in vii:
				if abs(i.first - cr[0] > 2 or abs(i.second - cr[2]) > 2) :
					wd.deleteRegion(i.first,i.second)
		render.update(*playerPos.toList())
		render.render(*playerPos.toList())

	def timer(self):
		self.clock.tick()

	def key_handler(self,keys):
		self.camera.strafe = self.camera.forward = self.camera.up= 0

		vel = 0.3
		if pygame.key.get_pressed()[pygame.K_z]:
			vel = 10

		if keys[ord('a')]:
			self.camera.MoveX(-vel)
		if keys[ord('d')]:
			self.camera.MoveX(vel)
		if keys[ord('w')]:
			self.camera.MoveZ(vel)
		if keys[ord('s')]:
			self.camera.MoveZ(-vel)
		if keys[ord('q')]:
			self.camera.Roll(-vel)
		if keys[ord('e')]:
			self.camera.Roll(vel)
		if keys[K_UP]:
			self.camera.Pitch(-vel)
		if keys[K_DOWN]:
			self.camera.Pitch(vel)
		if keys[K_LEFT]:
			self.camera.Yaw(-vel)
		if keys[K_RIGHT]:
			self.camera.Yaw(vel)
		if keys[ord('r')]:
			self.camera.reset()
		if keys[K_SPACE]:
			self.camera.MoveY(vel)
		if keys[K_LSHIFT]:
			self.camera.MoveY(-vel)

	def mouse_handler(self,mouse):
		pass

	def event_handler(self,events):
		global SCREEN_SIZE
		for event in events:
			if event.type == QUIT:
				self.running = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.running = False
				elif event.key == K_RETURN:
					try:
						print("return:",eval(input("Enter Command:/n")))
					except:
						print("Command failed")
					else:
						print("Command excuted")
				elif event.key == K_1:
					self.ID = 1
				elif event.key == K_2:
					self.ID = 2
				elif event.key == K_3:
					self.ID = 3
				elif event.key == K_4:
					self.ID = 4
				elif event.key == K_5:
					self.ID = 5
				elif event.key == K_6:
					self.ID = 6
				elif event.key == K_7:
					self.ID = 7
				elif event.key == K_8:
					self.ID = 8

			elif event.type == MOUSEBUTTONDOWN:
				if not self.hit: continue	
				#face = self.hit[3]
				#newPos = self.groundpos+ Vector3(DELTA[face])
				#self.groundpos = position + direction*t
				newPos = self.groundpos
				if self.hit and newPos:
					if event.button == 3:
						world.setBlock(newPos.x,newPos.y,newPos.z,self.ID)
					elif event.button == 1:
						world.setBlock(self.delPos.x,self.delPos.y,self.delPos.z,0)

			elif event.type == MOUSEMOTION:
				x,y =pygame.mouse.get_pos()
				self.camera.Yaw(0.15*(x-SCREEN_SIZE[0]//2))
				self.camera.Pitch(0.15*(y-SCREEN_SIZE[1]//2))
				pygame.mouse.set_pos((SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2))


	def drawText(self):
		fpssf = font.render("FPS: %d"%self.clock.get_fps(),True,(255,255,0))
		self.texture = createTexture(fpssf)
		renderTexture(self.texture[0],(0,0),(self.texture[1],self.texture[2]))
		deleteTexture(self.texture)

		xyz = font.render("X: %f Y: %f Z: %f"%(self.camera.position.x,
			self.camera.position.y,-self.camera.position.z),True,(255,255,0))
		xyztex = createTexture(xyz)
		renderTexture(xyztex[0],(0,SCREEN_SIZE[1]-xyztex[2]),(xyztex[1],xyztex[2]))
		deleteTexture(xyztex)

if __name__ == '__main__':
	game = Game()
	profile = 1 
	if profile:
		import cProfile
		cProfile.run('game.run()',sort =1)
	else:
		game.run()

	#import main
