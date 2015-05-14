import OpenGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utility import *
from Texture import *
import os
import re
class Skybox:


	def __init__(self,name,ext = 'tga'):

		path = os.path.join(name,'')
		name = re.split('[/|\\\\]',path)[-2]
		self.texture = {}
		for key,nm in zip(['FRONT','BACK','LEFT','RIGHT','UP','DOWN'],['ft','bk','lf','rt','up','dn']):
			sf = pygame.image.load(path+name+'_'+nm+'.'+ext)
			self.texture[key] = createTexture(sf)[0]


		x = 0
		y = 0
		z = 0
		width = 2048
		height = 2048
		length = 2048

		x = x - width  / 2
		y = y - height / 2
		z = z - length / 2

		self.list = glGenLists(1)

		glNewList(self.list,GL_COMPILE)

		glColor3f(255,255,255)
		glEnable(GL_TEXTURE_2D)

		glBindTexture(GL_TEXTURE_2D, self.texture["FRONT"])
		glBegin(GL_QUADS)
		glTexCoord2f(1, 0)
		glVertex3f(x, y, z+length)
		glTexCoord2f(1, 1)
		glVertex3f(x, y+height, z+length)
		glTexCoord2f(0, 1)
		glVertex3f(x+width, y+height, z+length)
		glTexCoord2f(0, 0)
		glVertex3f(x+width, y, z+length)
		glEnd()


		glBindTexture(GL_TEXTURE_2D, self.texture["BACK"])
		glBegin(GL_QUADS)
		glTexCoord2f(1, 0)
		glVertex3f(x+width, y, z)
		glTexCoord2f(1, 1)
		glVertex3f(x+width, y+height, z)
		glTexCoord2f(0, 1)
		glVertex3f(x, y+height, z)
		glTexCoord2f(0, 0)
		glVertex3f(x, y, z)
		glEnd()

		glBindTexture(GL_TEXTURE_2D, self.texture["LEFT"])
		glBegin(GL_QUADS)
		glTexCoord2f(1, 1)
		glVertex3f(x, y+height, z)
		glTexCoord2f(0, 1)
		glVertex3f(x, y+height, z+length)
		glTexCoord2f(0, 0)
		glVertex3f(x, y, z+length)
		glTexCoord2f(1, 0)
		glVertex3f(x, y, z)
		glEnd()

		glBindTexture(GL_TEXTURE_2D, self.texture["RIGHT"])
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex3f(x+width, y, z)
		glTexCoord2f(1, 0)
		glVertex3f(x+width, y, z+length)
		glTexCoord2f(1, 1)
		glVertex3f(x+width, y+height, z+length)
		glTexCoord2f(0, 1)
		glVertex3f(x+width, y+height, z)
		glEnd()

		glBindTexture(GL_TEXTURE_2D, self.texture["UP"])
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex3f(x+width, y+height, z)
		glTexCoord2f(1, 0)
		glVertex3f(x+width, y+height, z+length)
		glTexCoord2f(1, 1)
		glVertex3f(x, y+height, z+length)
		glTexCoord2f(0, 1)
		glVertex3f(x, y+height, z)
		glEnd()

		glBindTexture(GL_TEXTURE_2D, self.texture["DOWN"])
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex3f(x, y, z)
		glTexCoord2f(1, 0)
		glVertex3f(x, y, z+length)
		glTexCoord2f(1, 1)
		glVertex3f(x+width, y, z+length)
		glTexCoord2f(0, 1)
		glVertex3f(x+width, y, z)
		glEnd()

		glBindTexture(GL_TEXTURE_2D,0)
		glDisable(GL_TEXTURE_2D)

		glEndList()


	def render(self):
		glCallList(self.list)