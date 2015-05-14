import OpenGL
import numpy as np
from OpenGL.GL import *

class Tessellator:

	def __init__(self,bufsize=5000):
		self.bufferSize = bufsize
		self.drawMode = 0
		self.hasNormal = True
		self.hasColor = True
		self.hasTexture = True
		self.isDrawing = False

		self.reset()

	def startDrawingQuads(self):
		self.startDrawing(GL_QUADS)

	def startDrawing(self,mode):
		self.isDrawing = True
		self.reset()
		self.drawMode = mode
		self.hasNormal = False
		self.hasColor = False
		self.hasTexture = False

	def reset(self):

		self.vertexBuffer = np.empty(self.bufferSize* 3,dtype='f')

		if self.hasNormal:
			self.normalBuffer = np.empty(self.bufferSize*3,dtype='f')
		if self.hasTexture:
			self.textureBuffer = np.empty(self.bufferSize*2,dtype='f')
		if self.hasColor:
			self.colorBuffer = np.empty(self.bufferSize*4,dtype='f')

		self.numVertex = 0

	def addUV(self,u,v):
		self.hasTexture = True
		self.textureBuffer[self.numVertex*2] = u
		self.textureBuffer[self.numVertex*2+1] = v


	def addNormal(self,x,y,z):
		self.hasNormal = True
		self.normalBuffer[self.numVertex*3] = x
		self.normalBuffer[self.numVertex*3+1] = y 
		self.normalBuffer[self.numVertex*3+2] = z

	def addColor(self,r,g,b,a=0):
		self.hasColor = True
		self.colorBuffer[self.numVertex*4] = r
		self.colorBuffer[self.numVertex*4+1] = g 
		self.colorBuffer[self.numVertex*4+2] = b 
		self.colorBuffer[self.numVertex*4+3] = a

	def addColor256(self,r,g,b,a=0):
		self.addColor(r/256,g/256,b/256,a/256)

	def addVertex(self,x,y,z):
		self.vertexBuffer[self.numVertex*3] = x 
		self.vertexBuffer[self.numVertex*3+1] = y 
		self.vertexBuffer[self.numVertex*3+2] = z

		self.numVertex += 1

		if(self.numVertex%4==0 and self.numVertex+32 > self.bufferSize):
			self.draw()
			self.startDrawing(self.drawMode)

	def addVertexWithUV(self,x,y,z,u,v):
		self.addUV(u,v)
		self.addVertex(x,y,z)


	def draw(self):
		if not self.isDrawing:
			raise Exception("NO VERTEX NEEDDS TO DRAW, GTFO!")

		glEnableClientState(GL_VERTEX_ARRAY)
		glVertexPointer(3,GL_FLOAT,0,self.vertexBuffer)

		if self.hasColor:
			glEnableClientState(GL_COLOR_ARRAY)
			glColorPointer(4,GL_FLOAT,0,self.colorBuffer)

		if self.hasTexture:
			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
			glTexCoordPointer(2,GL_FLOAT,0,self.textureBuffer)

		if self.hasNormal:
			glEnableClientState(GL_NORMAL_ARRAY)
			glNormalPointer(3,GL_FLOAT,0,self.normalBuffer)

		glDrawArrays(self.drawMode, 0, self.numVertex)

		glDisableClientState(GL_VERTEX_ARRAY)

		if self.hasColor:
			glDisableClientState(GL_COLOR_ARRAY)

		if self.hasTexture:
			glDisableClientState(GL_TEXTURE_COORD_ARRAY)

		if self.hasNormal:
			glDisableClientState(GL_NORMAL_ARRAY)


		self.isDrawing = False

Tessellator.instance = Tessellator()
instance = Tessellator.instance

def haha():
	print(instance,Tessellator.instance)

if __name__ == '__main__':

	import OpenGL
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

	import time
	import numpy as np

	SCREEN_SIZE = 854,480

	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE,OPENGL|DOUBLEBUF)
	font = pygame.font.SysFont("Arial",18)

	glClearColor(111,111,111,0)
	glClearDepth(1)
	w = SCREEN_SIZE[0]
	h = SCREEN_SIZE[1]
	aspectRatio= w/h
	glViewport(0,0,w,h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(35.0, w/h, 1 , 10000.0)
	glEnable (GL_DEPTH_TEST)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	pygame.mouse.set_visible(True)
	pygame.mouse.set_pos((w//2,h//2))

	print(glGetString(GL_VERSION))
	running = True
	clock = pygame.time.Clock()

	camera = Camera()
	camera.position = Vector3(0,20,0)

	plane = glGenLists(1)

	glNewList(plane,GL_COMPILE)
	glPushMatrix()
	glTranslatef(-0.5,0,-0.5)
	glBegin(GL_LINES)
	for i in range(-50,50):
		glColor3ub(0,0,0)
		glVertex3f(-50, 0, i)
		glVertex3f(50, 0, i)
		glVertex3f(i, 0,-50)
		glVertex3f(i, 0, 50)
	glEnd()
	glPopMatrix()
	glEndList()

	def key_handler(keys):
		camera.strafe = camera.forward = camera.up= 0
		if keys[ord('a')]:
			camera.MoveX(-1)
		if keys[ord('d')]:
			camera.MoveX(1)
		if keys[ord('w')]:
			camera.MoveZ(1)
		if keys[ord('s')]:
			camera.MoveZ(-1)
		if keys[ord('q')]:
			camera.Roll(-1)
		if keys[ord('e')]:
			camera.Roll(1)
		if keys[K_UP]:
			camera.Pitch(-1)
		if keys[K_DOWN]:
			camera.Pitch(1)
		if keys[K_LEFT]:
			camera.Yaw(-1)
		if keys[K_RIGHT]:
			camera.Yaw(1)
		if keys[ord('r')]:
			camera.reset()
		if keys[K_SPACE]:
			camera.MoveY(1)
		if keys[K_LSHIFT]:
			camera.MoveY(-1)


	while running:
	
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				elif event.key == K_RETURN:
					try:
						print("return:",eval(input("Enter Command:\n")))
					except:
						print("Command failed")
					else:
						print("Command excuted")

			elif event.type == MOUSEBUTTONDOWN:
				pass
			elif event.type == MOUSEMOTION:
				x,y =pygame.mouse.get_pos()
				camera.Yaw(0.15*(x-SCREEN_SIZE[0]//2))
				camera.Pitch(0.15*(y-SCREEN_SIZE[1]//2))
				pygame.mouse.set_pos((SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2))

		key_handler(pygame.key.get_pressed())

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		camera.setPerspective()

		glPushMatrix()

		glCallList(plane)

		
		tes = Tessellator.instance
		tes.startDrawingQuads()
		tes.addColor(0,0,0,0)
		tes.addVertex(1,1,0)
		tes.addColor(1,0,0,1)
		tes.addVertex(100,1,0)
		tes.addColor(1,0,0,0)
		tes.addVertex(100,100,0)
		tes.addColor(1,0,0,0)
		tes.addVertex(1,100,0)
		tes.draw()



		fpssf = font.render("FPS: %d"%clock.get_fps(),True,(255,255,0))
		fpstex = createTexture(fpssf)
		renderTexture(fpstex[0],(0,0),(fpstex[1],fpstex[2]))

		xyz = font.render("X: %f Y: %f Z: %f"%(camera.position.x,
			camera.position.y,-camera.position.z),True,(255,255,0))
		xyztex = createTexture(xyz)
		renderTexture(xyztex[0],(0,SCREEN_SIZE[1]-xyztex[2]),(xyztex[1],xyztex[2]))

		glPopMatrix()
		
		clock.tick()
		pygame.display.flip()

	pygame.quit()
		
		

'''
class Tessellator2:

	convertQuadsToTriangles = False
	tryVBO = False

	def __init__(self,bufsize = 2097152 ):
		self.bufferSize = bufsize

		self.rawBufferIndex = 0

		self.isDrawing = False

		self.vboIndex = 0
		self.vboCount = 10

		if self.useVBO:
			self.vertexBuffers = glGenBuffers(self.vboCount)

		self.xOffset = 0
		self.yOffset = 0
		self.zOffset = 0

		self.drawMode = 0
		self.useVBO = False

		self.addedVertices = 0

		self.color = 0
		self.brightness = 0

		self.hasColor = False
		self.hasTexture = False
		self.hasBrightness = False

		self.textureU = 0
		self.textureV = 0


	def reset(self):
		self.vertexCount = 0
		self.byteBuffer.fill(0)
		self.rawBufferIndex = 0
		self.addedVertices = 0

	def startDrawingQuads(self):
		self.startDrawing(GL_QUADS)

	def startDrawing(self,mode):
		self.isDrawing = True
		self.reset()
		self.drawMode = mode
		self.hasNormals = False
		self.hasColor = False
		self.hasTexture = False
		self.hasBrightness = False
		self.isColorDisabled = False

	def setTextureUV(self,u,v):
		self.hasTexture = True
		self.textureU = u
		self.textureV = v

	def addVertexWithUV(self,x,y,z,u,v):
		self.setTextureUV(u,v)
		self.addVertex(x,y,z)

	def addVertex(self, x, y, z):

		self.addedVertices += 1

		if self.drawMode == GL_QUADS and self.convertQuadsToTriangles and self.addedVertices % 4 == 0:
			for i in range(2):
				offset = 8 * (3 - i)
				if self.hasTexture :
					self.rawBuffer[self.rawBufferIndex + 3] = self.rawBuffer[self.rawBufferIndex - offset + 3]
					self.rawBuffer[self.rawBufferIndex + 4] = self.rawBuffer[self.rawBufferIndex - offset + 4]
				if self.hasBrightness :
					self.rawBuffer[self.rawBufferIndex + 7] = self.rawBuffer[self.rawBufferIndex - offset + 7]
				if self.hasColor:
					self.rawBuffer[self.rawBufferIndex + 5] = self.rawBuffer[self.rawBufferIndex - offset + 5]
				self.rawBuffer[self.rawBufferIndex + 0] = self.rawBuffer[self.rawBufferIndex - offset + 0]
				self.rawBuffer[self.rawBufferIndex + 1] = self.rawBuffer[self.rawBufferIndex - offset + 1]
				self.rawBuffer[self.rawBufferIndex + 2] = self.rawBuffer[self.rawBufferIndex - offset + 2]
				self.vertexCount += 1
				self.rawBufferIndex += 8

		if self.hasTexture:
			self.rawBuffer[self.rawBufferIndex + 3] = self.textureU
			self.rawBuffer[self.rawBufferIndex + 4] = self.textureV

		if self.hasBrightness:
			self.rawBuffer[self.rawBufferIndex + 7] = self.brightness

		if self.hasColor:
			self.rawBuffer[self.rawBufferIndex + 5] = self.color

		if self.hasNormals:
			self.rawBuffer[self.rawBufferIndex + 6] = self.normal

		self.rawBuffer[self.rawBufferIndex + 0] = x + self.xOffset
		self.rawBuffer[self.rawBufferIndex + 1] = y + self.yOffset
		self.rawBuffer[self.rawBufferIndex + 2] = z + self.zOffset
		self.rawBufferIndex += 8
		self.vertexCount+=1

		if self.vertexCount % 4 == 0 and self.rawBufferIndex >= self.bufferSize - 32:
			self.draw()
			self.isDrawing = True

	def setTranslation(self, xoff, yoff, zoff):
		self.xOffset = xoff
		self.yOffset = yoff
		self.zOffset = zoff


	def addTranslation(self, xoff, yoff, zoff):
		self.xOffset += xoff
		self.yOffset += yoff
		self.zOffset += zoff

	def draw(self):

		if not self.isDrawing:
			raise Exception("Not tesselating!")
		else:

			self.isDrawing = False

			if self.vertexCount > 0:

				self.intBuffer.fill(0)
				self.intBuffer.put(self.rawBuffer, 0, self.rawBufferIndex)
				self.byteBuffer.position(0)
				self.byteBuffer.limit(self.rawBufferIndex * 4)

				if self.useVBO:
					self.vboIndex = (self.vboIndex + 1) % self.vboCount
					glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffers[self.vboIndex])
					glBufferData(GL_ARRAY_BUFFER, self.byteBuffer, GL_STREAM_DRAW)

				if self.hasTexture:
					if self.useVBO:
						glTexCoordPointer(2, GL_FLOAT, 32, 12)
					else:
						self.floatBuffer.position(3)
						glTexCoordPointer(2, 32, self.floatBuffer)

					glEnableClientState(GL_TEXTURE_COORD_ARRAY)


				if self.hasBrightness:
					#OpenGlHelper.setClientActiveTexture(OpenGlHelper.lightmapTexUnit)
					if self.useVBO:
						glTexCoordPointer(2, GL_SHORT, 32, 28)

					else:
						self.shortBuffer.position(14)
						glTexCoordPointer(2, 32, self.shortBuffer)

					glEnableClientState(GL_TEXTURE_COORD_ARRAY)
					#OpenGlHelper.setClientActiveTexture(OpenGlHelper.defaultTexUnit)


				if self.hasColor:
					if self.useVBO:
						glColorPointer(4, GL_UNSIGNED_BYTE, 32, 20)
					else:
						self.byteBuffer.position(20)
						glColorPointer(4, true, 32, self.byteBuffer)

					glEnableClientState(GL_COLOR_ARRAY)


				if self.hasNormals:
					if self.useVBO:
						glNormalPointer(GL_UNSIGNED_BYTE, 32, 24)
					else:
						self.byteBuffer.position(24)
						glNormalPointer(32, self.byteBuffer)

					glEnableClientState(GL_NORMAL_ARRAY)

				if self.useVBO:
					glVertexPointer(3, GL_FLOAT, 32, 0)

				else:
					self.floatBuffer.position(0)
					glVertexPointer(3, 32, self.floatBuffer)

				glEnableClientState(GL_VERTEX_ARRAY)

				if self.drawMode == GL_QUADS and self.convertQuadsToTriangles:
					glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)
				else:
					glDrawArrays(self.drawMode, 0, self.vertexCount)

				glDisableClientState(GL_VERTEX_ARRAY)

				if self.hasTexture:
					glDisableClientState(GL_TEXTURE_COORD_ARRAY)

				if self.hasBrightness:
					#OpenGlHelper.setClientActiveTexture(OpenGlHelper.lightmapTexUnit)
					glDisableClientState(GL_TEXTURE_COORD_ARRAY)
					#OpenGlHelper.setClientActiveTexture(OpenGlHelper.defaultTexUnit)

				if self.hasColor:
					glDisableClientState(GL_COLOR_ARRAY)

				if self.hasNormals:
					glDisableClientState(GL_NORMAL_ARRAY)



			idx = self.rawBufferIndex * 4
			self.reset()
			return idx
'''