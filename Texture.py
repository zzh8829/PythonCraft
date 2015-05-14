import OpenGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utility import *

import Tessellator

#import exp.test as test

def createTextureFromSurface(surface):
	#surf = pygame.Surface(surface.get_size(),pygame.SRCALPHA)
	#surf.blit(surface,(0,0))
	surf = surface
	width = surf.get_width()
	height = surf.get_height()
	data = pygame.image.tostring(surf,"RGBA",1)
	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D,texture)
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )

	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
	#glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,GL_RGBA,GL_UNSIGNED_BYTE, data)

	return texture,width,height

def createTextureFromFile(filename):
	return createTextureFromSurface(pygame.image.load(filename))

def createTexture(data):
	if isinstance(data,pygame.Surface):
		return createTextureFromSurface(data)
	elif isinstance(data,str):
		return createTextureFromFile(data)


def renderTexture(texture,pos,size,method="2D"):

	glColor3f(1,1,1)

	w,h = size

	if method == '2D':
		glEnable2D()
		x,y = pos
		z = 0
	else:
		if(len(pos)==3):
			x,y,z = pos
		else:
			x=pos[0]
			y=pos[1]
			z=0

	glEnable(GL_TEXTURE_2D)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	#glBlendFunc(GL_SRC_ALPHA, GL_ONE)
	glBindTexture(GL_TEXTURE_2D,texture)

	'''
	builder = test.MeshBuilder.getInstance()
	builder.begin(GL_QUADS)

	#print('wtf')

	builder.setTexCoord(0, 0)
	builder.addVertex(x, y, z)
	builder.setTexCoord(1, 0)
	builder.addVertex(x+w, y, z)
	builder.setTexCoord(1, 1)
	builder.addVertex(x+w, y+h, z)
	builder.setTexCoord(0, 1)
	builder.addVertex(x, y+h, z)

	builder.render()
	#print('hehe')

	'''
	tes = Tessellator.instance
	tes.startDrawingQuads()

	if method == '2D':
		tes.addUV(0, 0)
		tes.addVertex(x, y, z)
		tes.addUV(1, 0)
		tes.addVertex(x+w, y, z)
		tes.addUV(1, 1)
		tes.addVertex(x+w, y+h, z)
		tes.addUV(0, 1)
		tes.addVertex(x, y+h, z)
	else:
		tes.addUV(0, 0)
		tes.addVertex(x, y, z)
		tes.addUV(1, 0)
		tes.addVertex(x+w, y, z)
		tes.addUV(1, 1)
		tes.addVertex(x+w, y+h, z)
		tes.addUV(0, 1)
		tes.addVertex(x, y+h, z)
	
	tes.draw()
	#'''

	glBindTexture(GL_TEXTURE_2D,0)
	glDisable(GL_TEXTURE_2D)
	glDisable(GL_BLEND)


	if method == '2D': glDisable2D()

def deleteTexture(*args):
	glDeleteTextures(args[0])