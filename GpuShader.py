import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

class Shader:

	def __init__(self,typ):
		self.shader = glCreateShader(typ)

	def source(self,src):
		glShaderSource(self.shader,src)

	def compile(self):
		glCompileShader(self.shader)

	def check(self):
		print(glGetShaderInfoLog(self.shader).decode('u8'))