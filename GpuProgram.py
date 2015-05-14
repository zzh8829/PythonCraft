import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from GpuShader import *

from ZMath import *
from Utility import *

class Program:

	def __init__(self):

		self.program = glCreateProgram()

		self.uniforms = {}
		self.attributes = {}


	def attachShader(self,shader):
		glAttachShader(self.program,shader.shader)

	def detachShader(self,shader):
		glDetachShader(self.program,shader.shader)

	def link(self):
		glLinkProgram(self.program)

	def use(self):
		glUseProgram(self.program)

	def unuse(self):
		glUseProgram(0)

	def check(self):
		print(glGetProgramInfoLog(self.program))

	def getUniformLocation(self,uniform):

		res = glGetUniformLocation(self.program,uniform)
		self.uniforms[uniform] = res
		return res

	def getAttributeLocation(self,attr):
		res = glGetAttribLocation(self.program,attr)
		self.attributes[attr] = res
		return res

	def updateUniform(self,name,val):
		if name not in self.uniforms:
			self.getUniformLocation(name)

		single = 1
		if not isnumber(val):
			single = len(val)
		typ = 'f'
		if isinstance(val, int):
			typ = 'i'
		globals()['glUniform%d%s'%(single,typ)](self.uniforms[name],val)

	def updateUniformArray(self,name,val):
		if name not in self.uniforms:
			self.getUniformLocation(name)

		count = len(val)
		single = len(val[0])

		globals()['glUniform%dfv'%single](self.uniforms[name],count,val)


	def updateUniformMatrix(self,name,mats,transpose = 0):
		if name not in self.uniforms:
			self.getUniformLocation(name)

		if isinstance(mats,np.ndarray):
			count = len(mats)//16
			single = 4
		elif isinstance(mats, list):
			count = len(mats)
			single = int(sqrt(len(mats[0])))
			tmp = np.array(range(len(mats)*16),dtype='f')
			for i in range(len(mats)):
				for r in range(4):
					for c in range(4):
						tmp[i*16+r*4+c] = mats[i][r][c]
			mats = tmp

		globals()['glUniformMatrix%dfv'%single](self.uniforms[name],count,transpose,mats)






