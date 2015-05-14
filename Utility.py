import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *


RED   = (1.0,0.0,0.0,1.0)
GREEN = (0.0,0.0,1.0,1.0)
BLUE  = (0.0,1.0,0.0,1.0)
BLACK = (0.0,0.0,0.0,1.0)
WHITE = (1.0,1.0,1.0,1.0)


def glEnable2D():
	vPort = glGetIntegerv(GL_VIEWPORT)
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho( 0, vPort[2], 0, vPort[3], -1, 1)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	glDisable(GL_CULL_FACE);
	glClear(GL_DEPTH_BUFFER_BIT);

def glDisable2D():
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()
