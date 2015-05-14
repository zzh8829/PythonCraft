import zgui.guilocal as local
import pygame
import zgui
from .guiglobal import *
from .surface import *
from .color import *


def SafeSize(size):
	s = list(size)
	if size[0]<0: s[0] = 0
	if size[1]<0: s[1] = 0
	return int(s[0]),int(s[1])

def ResizeImage(img,size):
	if isinstance(img,zgui.surface.ExSurface): img = img.surface
	return zgui.surface.ExSurface(pygame.transform.scale(img,SafeSize(size)))

def CompareSize(s1,s2):
	if s1[0]>s2[0] and s1[1] > s2[1]:
		return True
	return False

def ValidateSize(s1,s2):
	if s1[0] < s2[0]:
		s1 = s2[0],s1[1]
	if s1[1] < s2[1]:
		s1= s1[0],s2[1]
	return s1

def MaxSize(s1,s2):
	return (min(s1[0],s2[0]),min(s1[1],s2[1]))

def pos_minus(p1,p2):
	return p1[0]-p2[0],p1[1]-p2[1]

def pos_plus(p1,p2):
	return p1[0]+p2[0],p1[1]+p2[1]


def pos_mul(p1,m):
	return p1[0]*m,p1[1]*m

def pos_div(p1,m):
	return p1[0]/m,p1[1]/m

def convex_hull(points):
	points = sorted(set(points))
	if len(points) <= 1:
		return points
	def cross(o, a, b):
		return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
	lower = []
	for p in points:
		while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
			lower.pop()
		lower.append(p)
	upper = []
	for p in reversed(points):
		while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
			upper.pop()
		upper.append(p)
	return lower[:-1] + upper[:-1]
