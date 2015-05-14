import OpenGL

import main
level = main.CLevel('saves/','Broville')
wd = level.getWorld()
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
from Camera import *
from Texture import *
from Skybox import *
from GpuProgram import *
from GpuShader import *

import threading

import exp.test as test
import exp.craft_net as cn

import Tessellator

import time
import numpy as np

#import renderer

SCREEN_SIZE = 854,480
SCREEN_FLAG = OPENGL|DOUBLEBUF|HWSURFACE
pygame.init()
font = pygame.font.SysFont("Arial",18)
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
vertices = np.array([0,0,0, 1,0,0, 0,1,0, 1,1,0,
					0,0,1, 1,0,1, 0,1,1, 1,1,1],dtype = 'f')

indices = np.array([2,3,7,6, 4,5,1,0, 0,1,3,2,
					1,5,7,3, 5,4,6,7, 4,0,2,6],dtype = 'i')

import os


class Texture:

	def __init__(self,path):
		self.path = path
		self.surface = pygame.image.load(path)
		self.width = self.surface.get_width()
		self.height = self.surface.get_height()
		self.raw = pygame.image.tostring(self.surface,"RGBA",1)
		self.texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D,self.texture)
		#glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		#glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		
		#glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		#glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0,GL_RGBA,GL_UNSIGNED_BYTE, self.raw)


class TextureManager:

	Textures = {}
	uv = {}

	__inited = False

	def __init__(self,folder):
		if self.__inited: raise Exception("U HAVE NO RIGHT")
		self.directory = folder
		self.__inited = True

		for root, dirs, files in os.walk(self.directory):
			for name in files:
				if name.endswith('png'):
					self.Textures[name[:-4]] = Texture(os.path.join(root,name))

		def tex(r,c,n=16):
			r = r/n
			c = 1-c/n
			d = 1/n
			return (r,c-d),(r+d,c-d),(r+d,c),(r,c)

		self.uv.update({
		"grass_top" : tex(0,0),
		"stone" : tex(1,0),
		"dirt" : tex(2,0),
		"grass_side" : tex(3,0),
		"oakwood" : tex(4,0),
		"stone_side" : tex(5,0),
		"stone_top" : tex(6,0),
		"wall" : tex(7,0),
		"tnt_side" : tex(8,0),
		"tnt_top" : tex(9,0) ,
		"tnt_bot" : tex(10,0),
		"water" : tex(14,13),
		"wood_side" : tex(4,1),
		"wood_top" : tex(5,1),
		"diamond" : tex(2,3),
		"bedrock" : tex(1,1),
		"cobblestone": tex(0,1),
		"glass" : tex(1,3),
		"sand" : tex(2,1),
		"gravel": tex(3,1),
		"leaves" : tex(4,3),
		})

	@classmethod
	def get(cls,name):
		return cls.Textures[name]

	@classmethod
	def getUV(cls,name):
		return cls.uv[name]

	@classmethod
	def generateUV(cls,*args):
		l = []
		for i in range(len(args)//2):
			for j in range(args[i*2+1]):
				l.append(cls.getUV(args[i*2]))
		return l 

TextureManager('textures')

terrain = createTexture('textures/terrain.png')



class Block:

	ID = [None for i in range(512)]
	#textures = [TextureManager.get('dirt')]*6
	colors = [[255,255,255,255] for i in range(6)]
	#uv = [(0,0)*4]*6

	def __init__(self,Id=0):
		Block.ID[Id] = self
		self.id = Id
		self.transparent = False

class NotAvailableBlock(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.id = -1

for i in range(512):
	NotAvailableBlock(i)

class Air(Block):
	pass
class Stone(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = [TextureManager.getUV('stone')]*6
class GrassBlock(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.colors = [[160,250,100]] + [[255,255,255]]*5
		self.uv = [TextureManager.getUV('grass_top'),TextureManager.getUV('dirt')]+[TextureManager.getUV('grass_side')]*4
class Dirt(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = [TextureManager.getUV('dirt')]*6
class Cobblestone(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('cobblestone',6)
class WoodPlanks(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = [TextureManager.getUV('oakwood')]*6
class TNT(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = [TextureManager.getUV('tnt_top'),TextureManager.getUV('tnt_bot')]+[TextureManager.getUV('tnt_side')]*4
class Diamond(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = [TextureManager.getUV('diamond')]*6
class Wood(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('wood_top',2,'wood_side',4)
class Bedrock(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('bedrock',6)
class Glass(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('glass',6)
		self.transparent = True
class Sand(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('sand',6)
class Water(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('water',6)
		self.transparent = True
class Gravel(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('gravel',6)
class Leaves(Block):
	def __init__(self,Id):
		super().__init__(Id)
		self.uv = TextureManager.generateUV('leaves',6)
		self.colors = [[48,122,16]]*6
		self.transparent = True


Air(0)
Stone(1)
GrassBlock(2)
Dirt(3)
Cobblestone(4)
WoodPlanks(5)
#Saplings(6)
Bedrock(7)
Water(8)
Water(9)
#Stationarywater(9)
#Lava(10)
#Stationarylava(11)
Sand(12)
Gravel(13)
#GoldOre(14)
#IronOre(15)
#CoalOre(16)
Wood(17)
Leaves(18)
#Sponge(19)
Glass(20)
#LapisLazuliOre(21)
#LapisLazuliBlock(22)
#Dispenser(23)
Sand(24)
#Sandstone(24)
#NoteBlock(25)
#Bed(26)
#PoweredRail(27)
#DetectorRail(28)
#StickyPiston(29)
#Cobweb(30)
#Grass(31)
#DeadBush(32)
#Piston(33)
#PistonExtension(34)
#Wool(35)
#BlockmovedbyPiston(36)
#Dandelion(37)
#Rose(38)
#BrownMushroom(39)
#RedMushroom(40)
#BlockofGold(41)
#Blockofron(42)
#DoubleSlabs(43)
#Slabs(44)
#Bricks(45)
TNT(46)
#Bookshelf(47)
#MossStone(48)
#Obsidian(49)
#Torch(50)
#Fire(51)
#MonsterSpawner(52)
#OakWoodStairs(53)
#Chest(54)
#RedstoneWire(55)
#DiamondOre(56)
#Blockofiamond(57)
#Craftingable(58)
#Wheat(59)
#Farmland(60)
#Furnace(61)
#BurningFurnace(62)
#SignPost(63)
#Woodenoor(64)
#Ladders(65)
#Rail(66)
#CobblestoneStairs(67)
#WallSign(68)
#Lever(69)
#StonePressurePlate(70)
#Ironoor(71)
#WoodenPressurePlate(72)
#RedstoneOre(73)
#GlowingRedstoneOre(74)
#Redstoneorchinactive(75)
#Redstoneorchactive(76)
#StoneButton(77)
#Snow(78)
#Ice(79)
#SnowBlock(80)
#Cactus(81)
#Clay(82)
#SugarCane(83)
#Jukebox(84)
#Fence(85)
#Pumpkin(86)
#Netherrack(87)
#SoulSand(88)
#Glowstone(89)
#NetherPortal(90)
#JackLantern(91)
#CakeBlock(92)
#RedstoneRepeaterinactive(93)
#RedstoneRepeateractive(94)
#LockedChest(95)
#Trapdoor(96)
#MonsterEgg(97)
#StoneBricks(98)
#HugeBrownMushroom(99)
#HugeRedMushroom(100)
#IronBars(101)
Glass(102)
#GlassPane(102)
#Melon(103)
#PumpkinStem(104)
#MelonStem(105)
#Vines(106)
#FenceGate(107)
#BrickStairs(108)
#StoneBrickStairs(109)
#Mycelium(110)
#LilyPad(111)
#NetherBrick(112)
#NetherBrickFence(113)
#NetherBrickStairs(114)
#NetherWart(115)
#Enchantmentable(116)
#BrewingStand(117)
#Cauldron(118)
#EndPortal(119)
#EndPortalBlock(120)
#EndStone(121)
#DragonEgg(122)


CHUNK_SIZE = 16
CHUNK_HEIGHT = 256
DELTA = [(0,1,0),(0,-1,0),(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)]
#DELTA = [(0,1,0),(0,-1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1)]


class Chunk:
	def __init__(self,world,x,z):
		self.world = world
		self.x = x
		self.z = z
		self.realX = x<<4
		self.realZ = z<<4

		self.needsRefresh = True

		self.list = 0

		#self.chunkData = cn.level.world.getChunk((self.x,0,self.z))
		self.chunkData = wd.getChunkData(self.x,self.z)

	def setBlock(self,x,y,z,ID):
		if y<0 or y>=CHUNK_HEIGHT or x < 0 or z < 0 or x>=CHUNK_SIZE or z>=CHUNK_SIZE:
			return -1
		self.chunkData.setBlockId(x,y,z,ID)
		self.needsRefresh = True
		if x == 0:
			self.world.getChunkFromChunkCoord(self.x-1,self.z).needsRefresh = True
		if x == 15:
			self.world.getChunkFromChunkCoord(self.x+1,self.z).needsRefresh = True
		if z == 0:
			self.world.getChunkFromChunkCoord(self.x,self.z-1).needsRefresh = True
		if z == 15:
			self.world.getChunkFromChunkCoord(self.x,self.z+1).needsRefresh = True

	def getBlock(self,x,y,z):
		if y<0 or y>=CHUNK_HEIGHT or x < 0 or z < 0 or x>=CHUNK_SIZE or z>=CHUNK_SIZE:
			return -1
		return self.chunkData.getBlockId(x,y,z)

	def refresh(self):

		self.needsRefresh = False

		self.list = glGenLists(1)
		glNewList(self.list,GL_COMPILE)
		glPushMatrix()
		glTranslatef(16*self.x,0,16*self.z)

		tes = test.MeshBuilder.getInstance()
		tes.begin(GL_QUADS)
		for x in range(16):
			for z in range(16):
				for y in range(128):
					ID = self.chunkData.getBlockId(x,y,z)
					block = Block.ID[ID]
					if ID:
						if block.id == -1:
							block = Block.ID[3]
						uvs =  block.uv
						colors = block.colors
	
						# Top
						if self.shouldRender(x,y,z,0, ID):
							tes.setNormal(0,1,0)

							tes.setTexCoord(uvs[0][0][0],uvs[0][0][1])
							tes.setColori(*colors[0])
							tes.addVertex(x,1+y,z)
							tes.setTexCoord(uvs[0][1][0],uvs[0][1][1])
							#tes.setColori(*colors[0])
							tes.addVertex(1+x,1+y,z)
							tes.setTexCoord(uvs[0][2][0],uvs[0][2][1])
							#tes.setColori(*colors[0])
							tes.addVertex(1+x,1+y,1+z)
							tes.setTexCoord(uvs[0][3][0],uvs[0][3][1])
							#tes.setColori(*colors[0])
							tes.addVertex(x,1+y,1+z)
						
						# Bot
						if self.shouldRender(x,y,z,1, ID):
							tes.setNormal(0,-1,0)

							tes.setTexCoord(uvs[1][0][0],uvs[1][0][1])
							tes.setColori(*colors[1])
							tes.addVertex(x,y,1+z)
							tes.setTexCoord(uvs[1][1][0],uvs[1][1][1])
							#tes.setColori(*colors[1])
							tes.addVertex(1+x,y,1+z)
							tes.setTexCoord(uvs[1][2][0],uvs[1][2][1])
							#tes.setColori(*colors[1])
							tes.addVertex(1+x,y,z)
							tes.setTexCoord(uvs[1][3][0],uvs[1][3][1])
							#tes.setColori(*colors[1])
							tes.addVertex(x,y,z)

						# Z Minus
						if self.shouldRender(x,y,z,2, ID):
							tes.setNormal(0,0,-1)
							tes.setTexCoord(uvs[2][0][0],uvs[2][0][1])
							tes.setColori(*colors[2])
							tes.addVertex(x,y,z)
							tes.setTexCoord(uvs[2][1][0],uvs[2][1][1])
							#tes.setColori(*colors[2])
							tes.addVertex(1+x,y,z)
							tes.setTexCoord(uvs[2][2][0],uvs[2][2][1])
							#tes.setColori(*colors[2])
							tes.addVertex(1+x,1+y,z)
							tes.setTexCoord(uvs[2][3][0],uvs[2][3][1])
							#tes.setColori(*colors[2])
							tes.addVertex(x,1+y,z)

						# X Plus
						if self.shouldRender(x,y,z,3, ID):
							tes.setNormal(1,0,0)
							tes.setTexCoord(uvs[3][0][0],uvs[3][0][1])
							tes.setColori(*colors[3])
							tes.addVertex(1+x,y,z)
							tes.setTexCoord(uvs[3][1][0],uvs[3][1][1])
							#tes.setColori(*colors[3])
							tes.addVertex(1+x,y,1+z)
							tes.setTexCoord(uvs[3][2][0],uvs[3][2][1])
							#tes.setColori(*colors[3])
							tes.addVertex(1+x,1+y,1+z)
							tes.setTexCoord(uvs[3][3][0],uvs[3][3][1])
							#tes.setColori(*colors[3])
							tes.addVertex(1+x,1+y,z)

						# Z Plus
						if self.shouldRender(x,y,z,4, ID):
							tes.setNormal(0,0,1)
							tes.setTexCoord(uvs[4][0][0],uvs[4][0][1])
							tes.setColori(*colors[4])
							tes.addVertex(1+x,y,1+z)
							tes.setTexCoord(uvs[4][1][0],uvs[4][1][1])
							#tes.setColori(*colors[4])
							tes.addVertex(x,y,1+z)
							tes.setTexCoord(uvs[4][2][0],uvs[4][2][1])
							#tes.setColori(*colors[4])
							tes.addVertex(x,1+y,1+z)
							tes.setTexCoord(uvs[4][3][0],uvs[4][3][1])
							#tes.setColori(*colors[4])
							tes.addVertex(1+x,1+y,1+z)

						# X Minus
						if self.shouldRender(x,y,z,5, ID):
							tes.setNormal(-1,0,0)
							tes.setTexCoord(uvs[5][0][0],uvs[5][0][1])
							tes.setColori(*colors[5])
							tes.addVertex(x,y,1+z)
							tes.setTexCoord(uvs[5][1][0],uvs[5][1][1])
							#tes.setColori(*colors[5])
							tes.addVertex(x,y,z)
							tes.setTexCoord(uvs[5][2][0],uvs[5][2][1])
							#tes.setColori(*colors[5])
							tes.addVertex(x,1+y,z)
							tes.setTexCoord(uvs[5][3][0],uvs[5][3][1])
							#tes.setColori(*colors[5])
							tes.addVertex(x,1+y,1+z)

			#n+=1
		tes.render()

		glPopMatrix()
		glEndList()
		

	def render(self):
		#if self.list:
		glCallList(self.list)

	def shouldRender(self,x,y,z,i,bid):
		y = y+DELTA[i][1]
		if y<0 or y>=256:
			return 0
		Id = wd.getBlockId(self.realX+x+DELTA[i][0],y,self.realZ+z+DELTA[i][2])
		return Id == 0 or (Block.ID[Id].transparent==True and Id!=bid)


def _floatToInt(n):
	return int(floor(n))

def floatToInt(*args):
	return tuple(map(_floatToInt,args))

class emptyChunk(Chunk):
	def __init__(self,world,x,z):
		pass

class World:

	def __init__(self):

		self.chunks = {}
		self.emptyChunk = emptyChunk(self,0,0)

		self.viewDistance = 6

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

	def genChunks(self,dx,dz):
		for x in range(-dx,dx):
			for z in range(-dz,dz):
				chunk = Chunk(self,x,z)
				self.chunks[x,z] = chunk

	def getChunkFromWorldCoord(self,x,z):
		return self.getChunkFromChunkCoord(x>>4,z>>4)

	def getChunkFromChunkCoord(self,x,z):
		if (x,z) in self.chunks:
			return self.chunks[x,z]
		return self.emptyChunk

	def render(self,viewPos):

		self.fpsCount+=1

		vx = int(viewPos.x)>>4
		vz = int(viewPos.z)>>4
		for x in range(-self.viewDistance,self.viewDistance):
			for z in range(-self.viewDistance,self.viewDistance):
				#if x**2+z**2 > self.viewDistance**2: continue
				nx,nz = x+vx,z+vz
				chunk = self.getChunkFromChunkCoord(nx,nz)
				if chunk == self.emptyChunk:
					chunk = Chunk(self,nx,nz)
					self.chunks[nx,nz] = chunk
				if chunk.needsRefresh:
					self.updateQueue.append((nx,nz))
					chunk.needsRefresh = False


		if self.updateQueue:
			#self.updateQueue.sort(key = lambda c: (c[0]-vx)**2+(c[1]-vz)**2)
			
			'''
			while self.updateQueue:
				x,z = self.updateQueue.pop(0)
				self.chunks[x,z].refresh()
				cnt+=1
				if cnt > 0:
					break
			'''
			if 1:
				self.updateQueue.sort(key = lambda c: (c[0]-vx)**2+(c[1]-vz)**2)
				chunk = self.chunks[self.updateQueue.pop(0)]
				chunk.refresh()

		glEnable(GL_TEXTURE_2D)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glAlphaFunc(GL_GREATER, 0.5);
		glEnable(GL_ALPHA_TEST)
		glBindTexture(GL_TEXTURE_2D,terrain[0])				
		for x in range(-self.viewDistance,self.viewDistance):
			for z in range(-self.viewDistance,self.viewDistance):
				if x**2+z**2 > self.viewDistance**2: continue
				nx,nz = x+vx,z+vz
				chunk = self.getChunkFromChunkCoord(nx,nz)
				if chunk != self.emptyChunk and chunk.list:
					glCallList(chunk.list)
		glDisable(GL_TEXTURE_2D)
		glDisable(GL_BLEND)

	def getBlock(self,x,y,z):
		#return self.getChunkFromWorldCoord(x,z).getBlock(x%16,y,z%16)
		return wd.getBlockId(x,y,z)

	def setBlock(self,x,y,z,ID):
		x,y,z = floatToInt(x,y,z)
		chunk = self.getChunkFromWorldCoord(x,z)
		if chunk is self.emptyChunk:
			chunk = Chunk(self,x>>4,z>>4)
			self.chunks[x>>4,z>>4] = chunk
		return chunk.setBlock(x%16,y,z%16,ID)

	def getRayHit(self,orgin,direction,length=100):
		for i in range(length*5):
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
render = main.CLevelRender(level)

class Game(object):
	def __init__(self):
		self.display_init()
		self.running = True
		self.clock = pygame.time.Clock()

		self.skybox = Skybox('textures/skybox/minecraft','png')
		self.camera = Camera()
		self.camera.setPosition((level.playerX,level.playerY,level.playerZ))
		#self.camera.setPosition(cn.level.playerPos)
		#self.camera.setPosition((0,20,0))

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
		gluPerspective(35.0, w/h, 0.5 , 10000.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		pygame.mouse.set_visible(True)
		pygame.mouse.set_pos((w//2,h//2))

		glEnable(GL_LIGHTING)
		glLightfv(GL_LIGHT1, GL_AMBIENT,(0,0,0,1,0 ))
		glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.95,0.95,0.95,1.0))
		glLightfv(GL_LIGHT1, GL_SPECULAR, (0.95,0.95,0.95,1.0))
		glLightfv(GL_LIGHT1, GL_POSITION, (128, 128.0 , 2.0, 1.0 ))
		glEnable(GL_LIGHT1)

		#glEnable(GL_FOG)
		glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
		glHint(GL_FOG_HINT, GL_DONT_CARE)
		glFogi(GL_FOG_MODE, GL_LINEAR)
		glFogf(GL_FOG_DENSITY, 0.35)
		glFogf(GL_FOG_START, 20.0)
		glFogf(GL_FOG_END, 60.0)

		print(glGetString(GL_VERSION))

		glFrontFace(GL_CW)
		glEnable(GL_ALPHA_TEST)
		glEnable (GL_DEPTH_TEST)

		glMaterialfv(GL_FRONT, GL_SPECULAR, (0.1,0.1,0.1, 1.0));
		glMaterialfv(GL_FRONT, GL_SHININESS, (10.0));
		glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);
		glEnable(GL_COLOR_MATERIAL);


	def renderScene(self,delta):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		self.camera.setPerspective()
		playerPos = self.camera.position.copy()
		playerPos.z = -playerPos.z
		
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
		tes = Tessellator.instance


		glPushMatrix()

		# Render Sky

		self.skybox.render()

		glDisable(GL_FOG)

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
		glBindTexture(GL_TEXTURE_2D,TextureManager.get("sun").texture)	
		tes.startDrawingQuads()
		tes.addVertexWithUV(-sunp, 300.0, -sunp, 0.0, 0.0)
		tes.addVertexWithUV(sunp, 300.0, -sunp, 1.0, 0.0)
		tes.addVertexWithUV(sunp, 300.0, sunp, 1.0, 1.0)
		tes.addVertexWithUV(-sunp, 300.0, sunp, 0.0, 1.0)
		tes.draw()
		glDisable(GL_BLEND)
		glPopMatrix()


		# Render Clouds
		glPushMatrix()
		glDisable(GL_CULL_FACE)

		glTranslatef(playerPos.x,playerPos.y,playerPos.z)


		predictY = self.camera.position.y
		spacing = 32
		amount = int(256 / spacing)
		glBindTexture(GL_TEXTURE_2D,TextureManager.get("clouds").texture)	
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
		tes.startDrawingQuads()

		#spacing*=2
		#amount=int(amount*1)
		

		for ix in range(-spacing*amount,spacing*amount,spacing):
			for iz in range(-spacing*amount,spacing*amount,spacing):
				tes.addColor(red, green, blue, 0.8)
				tes.addVertexWithUV((ix + 0), y, (iz + spacing), ((ix + 0) * small + cloudX), ((iz + spacing) * small + cloudZ))
				tes.addColor(red, green, blue, 0.8)
				tes.addVertexWithUV((ix + spacing), y, (iz + spacing), ((ix + spacing) * small + cloudX), ((iz + spacing) * small + cloudZ))
				tes.addColor(red, green, blue, 0.8)
				tes.addVertexWithUV((ix + spacing), y, (iz + 0), ((ix + spacing) * small + cloudX), ((iz + 0) * small + cloudZ))
				tes.addColor(red, green, blue, 0.8)
				tes.addVertexWithUV((ix + 0), y, (iz + 0), ((ix + 0) * small + cloudX), ((iz + 0) * small + cloudZ))
		tes.draw()
		glColor4f(1.0, 1.0, 1.0, 1.0)
		glDisable(GL_BLEND)
		#glEnable(GL_CULL_FACE)
		glPopMatrix()



		#glEnable(GL_FOG)

		# Render Plane
		#glCallList(self.plane)
		#test.CUBE()

		# Render World
		#render.render(*floatToInt(*playerPos.toList()))
		world.render(playerPos)

		glPushMatrix()
		if self.groundpos:
			glTranslatef(*floatToInt(*self.groundpos.toList()))
			glCallList(selectBlock)

		glPopMatrix()

		self.drawText()
		glPopMatrix()

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
		for event in events:
			if event.type == QUIT:
				self.running = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.running = False
				elif event.key == K_RETURN:
					try:
						print("return:",eval(input("Enter Command:\n")))
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
		fpstex = createTexture(fpssf)
		renderTexture(fpstex[0],(0,0),(fpstex[1],fpstex[2]))
		#deleteTexture(fpstex)

		xyz = font.render("X: %f Y: %f Z: %f"%(self.camera.position.x,
			self.camera.position.y,-self.camera.position.z),True,(255,255,0))
		xyztex = createTexture(xyz)
		renderTexture(xyztex[0],(0,SCREEN_SIZE[1]-xyztex[2]),(xyztex[1],xyztex[2]))
		#deleteTexture(xyztex)

if __name__ == '__main__':
	game = Game()
	import cProfile
	cProfile.run('game.run()',sort =1)
	#game.run()

	#import main
