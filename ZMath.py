#=================================
#==== 3DMath Computing lib  ======
#========  Zihao Zhang  ==========
#======  Copyright @2013 =========
#=================================

import numpy as np
from math import *

def invSqrt(n):
	return 1/sqrt(n)

def isnumber(n):
	return isinstance(n, (float,int,complex))

class Vector3(object):
	"""Vector3 Class"""

	def __init__(self,*args):
		if len(args)==0:
			self.x = 0
			self.y = 0
			self.z = 0
		elif len(args)==1:
			if isinstance(args[0], Vector3):
				self.x = args[0].x
				self.y = args[0].y
				self.z = args[0].z
			elif isinstance(args[0], (list,tuple)):
				self.x = args[0][0]
				self.y = args[0][1]
				self.z = args[0][2]
			else:
				raise NotImplemented(" error")

		elif len(args)==3:
			self.x,self.y,self.z = args

		else:
			raise NotImplemented(" error")

	def __mul__(self,other):
		if isinstance(other,Vector3):
			return self.crossProduct(other)
		elif isinstance(other,Quaternion):
			return self.rotate(other)
		elif isnumber(other):
			return Vector3(
				self.x*other,
				self.y*other,
				self.z*other
				)


	def __div__(self,other):
		if isnumber(other):
			return self.__mul__(1/other)

	def __rmul__(self,other):
		return self.__mul__(other)

	def __rdiv__(self,other):
		return self.__div__(other)

	def __neg__(self):
		return Vector3(-self.x,-self.y,-self.z)

	def __add__(self,other):
		return Vector3(
			self.x+other.x,
			self.y+other.y,
			self.z+other.z
			)

	def __sub__(self,other):
		return self.__add__(-other)

	def __str__(self):
		return "Vector3(%.2f, %.2f, %.2f)"%(self.x,self.y,self.z)

	def toList(self):
		return [self.x,self.y,self.z]

	def normalise(self):
		scale = 1/self.length()
		self.x *= scale
		self.y *= scale
		self.z *= scale

	def normalised(self):
		scale = 1/self.length()
		return Vector3(
			self.x * scale,
			self.y * scale,
			self.z * scale
		)

	def crossProduct(self,other):
		return Vector3(
			self.y*other.z - self.z*other.y,
			self.z*other.x - self.x*other.z,
			self.x*other.y - self.y*other.x
			)

	def dotProduct(self,other):
		return self.x*other.x + self.y*other.y +self.z*other.z

	def rotate(self,quat):
		u = Vector3(quat.x,quat.y,quat.z)
		s = quat.w
		return 2*u.dotProduct(self)*u + (s*s - u.dotProduct(u))*self + 2*s*u.crossProduct(self)

	def length(self):
		return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)

	def copy(self):
		return Vector3(self)

	@staticmethod
	def ZERO():
		return Vector3(0,0,0)

class Vector2(object):
	"""Vector2 Class"""
	def __init__(self):
		self.x = 0
		self.y = 0

class Quaternion(object):
	"""Quaternion Class"""

	def __init__(self,*args):
		if len(args)==0:
			self.w = 1
			self.x = 0
			self.y = 0
			self.z = 0
		elif len(args)==1:
			if isinstance(args[0], Matrix4):
				self.fromMatrix(args[0])
			elif isinstance(args[0], Quaternion):
				self.fromQuaternion(args[0])
		elif len(args)==2:
			self.fromAxisAngle(*args)
		elif len(args)==3:
			self.fromAngle(*args)
		elif len(args)==4:
			self.w,self.x,self.y,self.z = args

	def __add__(self,other):
		return Quaternion(
			self.w+other.w,
			self.x+other.x,
			self.y+other.y,
			self.z+other.z
		)

	def __sub__(self,other):
		return Quaternion(
			self.w-other.w,
			self.x-other.x,
			self.y-other.y,
			self.z-other.z
		)

	def __mul__(self,other):

		if isinstance(other,Vector3):
			return self.rotate(other)

		elif isinstance(other,Quaternion):
			other.normalise()
			return Quaternion(
				self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
				self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
				self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z,
				self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x
			)
		elif isnumber(other):
			return Quaternion(
				self.w*other,
				self.x*other,
				self.y*other,
				self.z*other
			)

	def __getitem__(self,idx):
		if idx == 0:
			return self.x
		elif idx == 1:
			return self.y
		elif idx == 2:
			return self.z
		elif idx == 3:
			return self.w
		else:
			raise Exception("Invalid index")

	def __setitem__(self,idx,val):
		if idx == 0:
			self.x = val
		elif idx == 1:
			self.y = val
		elif idx == 2:
			self.z = val
		elif idx == 3:
			self.w = val
		else:
			raise Exception("Invalid index")


	def __str__(self):
		return "Quaternion.XYZW: %.2f %.2f %.2f %.2f"%(self.x,self.y,self.z,self.w)

	def fromMatrix(self,mat):
		trace = mat[0][0]+mat[1][1]+mat[2][2]
		root = 0.0

		if trace > 0:
			root = sqrt(trace + 1.0)
			w = 0.5*root
			root = 0.5/root
			self.x = (mat[2][1]-mat[1][2])*root
			self.y = (mat[0][2]-mat[2][0])*root
			self.z = (mat[1][0]-mat[0][1])*root
		else:
			next = [ 1, 2, 0 ]
			i = 0
			if  mat[1][1] > mat[0][0]:
				i = 1
			if mat[2][2] > mat[i][i]:
				i = 2
			j = next[i]
			k = next[j]

			root = sqrt(mat[i][i]-mat[j][j]-mat[k][k] + 1.0)

			self[i] = 0.5*root
			root = 0.5/root
			self.w = (mat[k][j]-mat[j][k])*root
			self[j] = (mat[j][i]+mat[i][j])*root
			self[k] = (mat[k][i]+mat[i][k])*root

	def fromAngle(self,x,y,z):
		ang = x*0.5
		sr = sin(ang)
		cr = cos(ang)
		ang = y*0.5
		sp = sin(ang)
		cp = cos(ang)
		ang = z*0.5
		sy = sin(ang)
		cy = cos(ang)
		cpcy = cp * cy
		spcy = sp * cy
		cpsy = cp * sy
		spsy = sp * sy
		self.x = sr * cpcy - cr * spsy
		self.y = cr * spcy + sr * cpsy
		self.z = cr * cpsy - sr * spcy
		self.w = cr * cpcy + sr * spsy
		self.normalise()

	def fromAxisAngle(self,angle,v):
		if v.length() == 0:
			return Quaternion.IDENTITY()

		half = angle* 0.5
		v2 = v.normalised()
		sinv = sin(half)
		cosv = cos(half)

		self.x = v2.x * sinv
		self.y = v2.y * sinv
		self.z = v2.z * sinv
		self.w = cosv

		self.normalise()

	def toAxisAngle(self):
		q = Quaternion(self.w,self.x,self.y,self.z)
		if abs(self.w) > 1:
			q.normalise()
		axis = None
		angle = 2*acos(q.w)
		den = sqrt(1-q.w*q.w)
		if den > 0.0001:
			axis = Vector3(q.x/den,q.y/den,q.z/den)
		else:
			axis = Vector3(1,0,0)
		return angle,axis

	def fromQuaternion(self,quat):
		self.__init__(quat.w,quat.x,quat.y,quat.z)

	def toMatrix(self):
		matrix = Matrix4()
		matrix[0][0] = 1 - 2 * (self.y**2 + self.z**2)
		matrix[0][1] = 2 * (self.x*self.y + self.z*self.w)
		matrix[0][2] = 2 * (self.x*self.z - self.y*self.w)
		matrix[0][3] = 0
		matrix[1][0] = 2 * (self.x*self.y - self.z*self.w)
		matrix[1][1] = 1 - 2 * (self.x**2 + self.z**2)
		matrix[1][2] = 2 * (self.z*self.y + self.x*self.w)
		matrix[1][3] = 0
		matrix[2][0] = 2 * (self.x*self.z + self.y*self.w)
		matrix[2][1] = 2 * (self.y*self.z - self.x*self.w)
		matrix[2][2] = 1 - 2 * (self.x**2 + self.y**2)
		matrix[2][3] = 0
		matrix[3][0] = 0
		matrix[3][1] = 0
		matrix[3][2] = 0
		matrix[3][3] = 1
		return matrix

	def computeW(self):
		t = 1.0 - (self.x*self.x+self.y*self.y+self.z*self.z)
		if t > 0: self.w = -sqrt(t)
		else : self.w = 0

	def rotate(self,v):
		temp = Vector3(self.x,self.y,self.z)
		uv= temp*v
		uuv= temp*uv
		uv= uv*self.w*2.0
		uuv= uuv*2.0
		return uv + v + uuv

	def norm(self):
		return self.w*self.w+self.x*self.x+self.y*self.y+self.z*self.z

	def normalise(self):
		scale = 1/self.length()
		self.w *= scale
		self.x *= scale
		self.y *= scale
		self.z *= scale

	def length(self):
		return sqrt(self.w*self.w+self.x*self.x+self.y*self.y+self.z*self.z)

	def inverse(self):
		norm = self.norm()
		if norm !=0  :
			invNorm = 1/norm
			return Quaternion(w*invNorm,-x*invNorm,-y*invNorm,-z*invNorm)
		else:
			return Quaternion(0,0,0,0)

	def conjugate(self):
		return Quaternion(self.w,-self.x,-self.y,-self.z)

	@staticmethod
	def IDENTITY():
		return Quaternion(1,0,0,0)

	@staticmethod
	def ZERO():
		return Quaternion(0,0,0,0)


class Matrix4(object):

	POSMAP = {
		'm11' : (0,0),
		'm21' : (1,0),
		'm31' : (2,0),
		'm41' : (3,0),
		'm12' : (0,1),
		'm22' : (1,1),
		'm32' : (2,1),
		'm42' : (3,1),
		'm13' : (0,2),
		'm23' : (1,2),
		'm33' : (2,2),
		'm43' : (3,2),
		'm14' : (0,3),
		'm24' : (1,3),
		'm34' : (2,3),
		'm44' : (3,3),
	}

	def __init__(self,*args):
		self._data = np.array([0 for i in range(16)],dtype='f')
		self._data = np.reshape(self._data,(4,4))
		if len(args) == 1:
			if isinstance(args[0],(list,tuple)):
				self.fromList(args[0])
			elif isinstance(args[0],Quaternion):
				self.fromQuaternion(args[0])
			elif isinstance(args[0],Matrix4):
				self.fromMatrix(args[0])
		elif len(args) == 16:
			self.__init__(args)

	def __mul__(self,other):

		if isinstance(other,Matrix4):
			return self.mul_matrix(other)

	def __len__(self):
		return 16

	def __str__(self):
		return self._data.__str__()

	def __getattribute__(self,attr):
		if attr == '__class__':
			return np.ndarray
		return super().__getattribute__(attr)

	def __getattr__(self,attr):
		if attr in self.POSMAP.keys():
			return self._data[self.POSMAP[attr][0]][self.POSMAP[attr][1]]
		elif '_data' in self.__dict__ and attr in dir(self._data):
			return getattr(self._data,attr)
		else:
			raise Exception("Attribute Error!")

	def __setattr__(self,attr,val):
		if attr in self.POSMAP.keys():
			self._data[self.POSMAP[attr][0]][self.POSMAP[attr][1]] = val
		elif '_data' in self.__dict__ and attr in dir(self._data):
			setattr(self._data,attr,val)
		else:
			self.__dict__[attr] = val

	def __getitem__(self,idx):
		return self._data.__getitem__(idx)

	def __setitem__(self,idx,val):
		return self._data.__setitem__(idx,val)

	def determinant(self):
		return self[0][0] * self[1][1] * self[2][2] * self[3][3] \
				- self[0][0] * self[1][1] * self[2][3] * self[3][2] \
				+ self[0][0] * self[1][2] * self[2][3] * self[3][1] \
				- self[0][0] * self[1][2] * self[2][1] * self[3][3] \
				+ self[0][0] * self[1][3] * self[2][1] * self[3][2] \
				- self[0][0] * self[1][3] * self[2][2] * self[3][1] \
				- self[0][1] * self[1][2] * self[2][3] * self[3][0] \
				+ self[0][1] * self[1][2] * self[2][0] * self[3][3] \
				- self[0][1] * self[1][3] * self[2][0] * self[3][2] \
				+ self[0][1] * self[1][3] * self[2][2] * self[3][0] \
				- self[0][1] * self[1][0] * self[2][2] * self[3][3] \
				+ self[0][1] * self[1][0] * self[2][3] * self[3][2] \
				+ self[0][2] * self[1][3] * self[2][0] * self[3][1] \
				- self[0][2] * self[1][3] * self[2][1] * self[3][0] \
				+ self[0][2] * self[1][0] * self[2][1] * self[3][3] \
				- self[0][2] * self[1][0] * self[2][3] * self[3][1] \
				+ self[0][2] * self[1][1] * self[2][3] * self[3][0] \
				- self[0][2] * self[1][1] * self[2][0] * self[3][3] \
				- self[0][3] * self[1][0] * self[2][1] * self[3][2] \
				+ self[0][3] * self[1][0] * self[2][2] * self[3][1] \
				- self[0][3] * self[1][1] * self[2][2] * self[3][0] \
				+ self[0][3] * self[1][1] * self[2][0] * self[3][2] \
				- self[0][3] * self[1][2] * self[2][0] * self[3][1] \
				+ self[0][3] * self[1][2] * self[2][1] * self[3][0] \

	def fromList(self,l):
		if len(l) == 4:
			for i in range(4):
				for j in range(4):
					self[i][j] = l[i][j]
		elif len(l) == 16:
			for i in range(4):
				for j in range(4):
					self[i][j] = l[i*4+j]


	def fromQuaternion(self,quat):
		angle,axis = quat.toAxisAngle()
		return self.fromAxisAngle(angle,axis)

	def fromAxisAngle(self,angle,axis):
		cosa = cos(-angle)
		sina = sin(-angle)
		t = 1.0 - cosa
		axis.normalise()
		self.fromList([
			t * axis.x * axis.x + cosa, t * axis.x * axis.y - sina * axis.z, t * axis.x * axis.z + sina * axis.y, 0.0,
			t * axis.x * axis.y + sina * axis.z, t * axis.y * axis.y + cosa, t * axis.y * axis.z - sina * axis.x, 0.0,
			t * axis.x * axis.z - sina * axis.y, t * axis.y * axis.z + sina * axis.x, t * axis.z * axis.z + cosa, 0.0,
			0, 0, 0, 1]
		)

	def fromMatrix(self,mat):
		for i in range(4):
			for j in range(4):
				self[i][j] = mat[i][j]

	def toQuaternion(self):
		s = sqrt(abs(self[0][0] + self[1][1] + self[2][2] + self[3][3]))
		if s == 0.0:
			x = abs(self[2][1] - self[1][2])
			y = abs(self[0][2] - self[2][0])
			z = abs(self[1][0] - self[0][1])
			if  (x >= y) and (x >= z):
				return Quaternion(0.0, 1.0, 0.0, 0.0)
			elif (y >= x) and (y >= z):
				return Quaternion(0.0, 0.0, 1.0, 0.0)
			else:
				return Quaternion(0.0, 0.0, 0.0, 1.0)

		q = Quaternion(
			0.5 * s,
			-(self[2][1] - self[1][2]) / (2.0 * s),
			-(self[0][2] - self[2][0]) / (2.0 * s),
			-(self[1][0] - self[0][1]) / (2.0 * s)
			)
		q.normalise()
		return q

	def toArray(self):
		return self._data.copy()

	def toList(self):
		return [ i for i in self._data.flatten() ]


	def inverse(self):

		mat = Matrix4(self)

		colIdx = [ 0, 0, 0, 0 ]
		rowIdx = [ 0, 0, 0, 0 ]
		pivotIdx = [-1, -1, -1, -1 ]

		inv = [[c for c in r] for r in self ]

		icol = 0
		irow = 0
		for i in range(4):
			maxPivot = 0
			for j in range(4):
				if pivotIdx[j] != 0:
					for k in range(4):
						if pivotIdx[k] == -1:
							absVal = abs(inv[j][k])
							if absVal > maxPivot:
								maxPivot = absVal
								irow = j
								icol = k
						elif pivotIdx[k] > 0:
							return mat

			pivotIdx[icol]+=1

			if irow != icol:
				for k in range(4):
					tmp = inv[irow][k]
					inv[irow][k] = inv[icol][k]
					inv[icol][k] = tmp

			rowIdx[i] = irow
			colIdx[i] = icol

			pivot = inv[icol][icol]
			if pivot == 0 :
				raise Exception("Matrix is singular")

			invPivot = 1.0 / pivot
			inv[icol][icol] = 1.0
			for k in range(4):
				inv[icol][k] *= invPivot

			for j in range(4):
				if icol != j:
					tmp = inv[j][icol]
					inv[j][icol] = 0
					for k in range(4):
						inv[j][k] -= inv[icol][k] * tmp

		for j in reversed(range(4)):
			ir = rowIdx[j]
			ic = colIdx[j]
			for k in range(4):
				tmp = inv[k][ir]
				inv[k][ir] = inv[k][ic]
				inv[k][ic] = tmp

		mat.fromList(inv)
		return mat

	def mul_matrix(a,b):
		return Matrix4([[
			a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0] + a[0][3] * b[3][0],
			a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1] + a[0][3] * b[3][1],
			a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2] + a[0][3] * b[3][2],
			a[0][0] * b[0][3] + a[0][1] * b[1][3] + a[0][2] * b[2][3] + a[0][3] * b[3][3]
			], [
			a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0] + a[1][3] * b[3][0],
			a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1] + a[1][3] * b[3][1],
			a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2] + a[1][3] * b[3][2],
			a[1][0] * b[0][3] + a[1][1] * b[1][3] + a[1][2] * b[2][3] + a[1][3] * b[3][3]
			], [
			a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0] + a[2][3] * b[3][0],
			a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1] + a[2][3] * b[3][1],
			a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2] + a[2][3] * b[3][2],
			a[2][0] * b[0][3] + a[2][1] * b[1][3] + a[2][2] * b[2][3] + a[2][3] * b[3][3],
			], [
			a[3][0] * b[0][0] + a[3][1] * b[1][0] + a[3][2] * b[2][0] + a[3][3] * b[3][0],
			a[3][0] * b[0][1] + a[3][1] * b[1][1] + a[3][2] * b[2][1] + a[3][3] * b[3][1],
			a[3][0] * b[0][2] + a[3][1] * b[1][2] + a[3][2] * b[2][2] + a[3][3] * b[3][2],
			a[3][0] * b[0][3] + a[3][1] * b[1][3] + a[3][2] * b[2][3] + a[3][3] * b[3][3]
			]])

	@staticmethod
	def IDENTITY():
		return Matrix4(
			[1, 0, 0, 0,
			 0, 1, 0, 0,
			 0, 0, 1, 0,
			 0, 0, 0, 1 ]
		)

	@staticmethod
	def ZERO():
		return Matrix4(
			[0, 0, 0, 0,
			 0, 0, 0, 0,
			 0, 0, 0, 0,
			 0, 0, 0, 0]
		)


def quaternion2matrix(q):
	xx = q[0] * q[0]
	yy = q[1] * q[1]
	zz = q[2] * q[2]
	xy = q[0] * q[1]
	xz = q[0] * q[2]
	yz = q[1] * q[2]
	wx = q[3] * q[0]
	wy = q[3] * q[1]
	wz = q[3] * q[2]
	return [[ 1.0 - 2.0 * (yy + zz)	,		2.0 * (xy + wz),		2.0 * (xz - wy), 0.0],
			[		2.0 * (xy - wz)	, 1.0 - 2.0 * (xx + zz),		2.0 * (yz + wx), 0.0],
			[		2.0 * (xz + wy)	,	 	2.0 * (yz - wx),  1.0 - 2.0 * (xx + yy), 0.0],
			[					0.0	, 					0.0,					0.0, 1.0]]
def euler2matrix(e):
	#euler is assumed to be a float[3], with YAW, PITCH, ROLL (in this order) in degrees
	return matrix_multiply(
			matrix_multiply(
				matrix_rotate_z(e[0]/180*math.pi),
				matrix_rotate_y(e[1]/180*math.pi)),
			matrix_rotate_x(e[2]/180*math.pi)		)

def matrix2quaternion(m):
	s = math.sqrt(abs(m[0][0] + m[1][1] + m[2][2] + m[3][3]))
	if s == 0.0:
		x = abs(m[2][1] - m[1][2])
		y = abs(m[0][2] - m[2][0])
		z = abs(m[1][0] - m[0][1])
		if	 (x >= y) and (x >= z): return 1.0, 0.0, 0.0, 0.0
		elif (y >= x) and (y >= z): return 0.0, 1.0, 0.0, 0.0
		else:											 return 0.0, 0.0, 1.0, 0.0
	return quaternion_normalize([
		-(m[2][1] - m[1][2]) / (2.0 * s),
		-(m[0][2] - m[2][0]) / (2.0 * s),
		-(m[1][0] - m[0][1]) / (2.0 * s),
		0.5 * s,
		])

def quaternion_normalize(q):
	l = math.sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3])
	return q[0] / l, q[1] / l, q[2] / l, q[3] / l

def quaternion_multiply(q1, q2):
	r = [
		q2[3] * q1[0] + q2[0] * q1[3] + q2[1] * q1[2] - q2[2] * q1[1],
		q2[3] * q1[1] + q2[1] * q1[3] + q2[2] * q1[0] - q2[0] * q1[2],
		q2[3] * q1[2] + q2[2] * q1[3] + q2[0] * q1[1] - q2[1] * q1[0],
		q2[3] * q1[3] - q2[0] * q1[0] - q2[1] * q1[1] - q2[2] * q1[2],
		]
	d = math.sqrt(r[0] * r[0] + r[1] * r[1] + r[2] * r[2] + r[3] * r[3])
	r[0] /= d
	r[1] /= d
	r[2] /= d
	r[3] /= d
	return r

def matrix_translate(m, v):
	m[3][0] += v[0]
	m[3][1] += v[1]
	m[3][2] += v[2]
	return m

def matrix_multiply(b, a):
	return [ [
		a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0],
		a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1],
		a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2],
		0.0,
		], [
		a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0],
		a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1],
		a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2],
		0.0,
		], [
		a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0],
		a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1],
		a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2],
		 0.0,
		], [
		a[3][0] * b[0][0] + a[3][1] * b[1][0] + a[3][2] * b[2][0] + b[3][0],
		a[3][0] * b[0][1] + a[3][1] * b[1][1] + a[3][2] * b[2][1] + b[3][1],
		a[3][0] * b[0][2] + a[3][1] * b[1][2] + a[3][2] * b[2][2] + b[3][2],
		1.0,
		] ]

def matrix_invert(m):
	det = (m[0][0] * (m[1][1] * m[2][2] - m[2][1] * m[1][2])
		 - m[1][0] * (m[0][1] * m[2][2] - m[2][1] * m[0][2])
		 + m[2][0] * (m[0][1] * m[1][2] - m[1][1] * m[0][2]))
	if det == 0.0: return None
	det = 1.0 / det
	r = [ [
			det * (m[1][1] * m[2][2] - m[2][1] * m[1][2]),
		  - det * (m[0][1] * m[2][2] - m[2][1] * m[0][2]),
			det * (m[0][1] * m[1][2] - m[1][1] * m[0][2]),
			0.0,
		], [
		  - det * (m[1][0] * m[2][2] - m[2][0] * m[1][2]),
			det * (m[0][0] * m[2][2] - m[2][0] * m[0][2]),
		  - det * (m[0][0] * m[1][2] - m[1][0] * m[0][2]),
			0.0
		], [
			det * (m[1][0] * m[2][1] - m[2][0] * m[1][1]),
		  - det * (m[0][0] * m[2][1] - m[2][0] * m[0][1]),
			det * (m[0][0] * m[1][1] - m[1][0] * m[0][1]),
			0.0,
		] ]
	r.append([
		-(m[3][0] * r[0][0] + m[3][1] * r[1][0] + m[3][2] * r[2][0]),
		-(m[3][0] * r[0][1] + m[3][1] * r[1][1] + m[3][2] * r[2][1]),
		-(m[3][0] * r[0][2] + m[3][1] * r[1][2] + m[3][2] * r[2][2]),
		1.0,
		])
	return r

def matrix_rotate_x(angle):
	cos = math.cos(angle)
	sin = math.sin(angle)
	return [
		[1.0,	0.0, 0.0, 0.0],
		[0.0,	cos, sin, 0.0],
		[0.0,  -sin, cos, 0.0],
		[0.0,	0.0, 0.0, 1.0],
		]

def matrix_rotate_y(angle):
	cos = math.cos(angle)
	sin = math.sin(angle)
	return [
		[cos, 0.0, -sin, 0.0],
		[0.0, 1.0,	0.0, 0.0],
		[sin, 0.0,	cos, 0.0],
		[0.0, 0.0,	0.0, 1.0],
		]

def matrix_rotate_z(angle):
	cos = math.cos(angle)
	sin = math.sin(angle)
	return [
		[ cos, sin, 0.0, 0.0],
		[-sin, cos, 0.0, 0.0],
		[ 0.0, 0.0, 1.0, 0.0],
		[ 0.0, 0.0, 0.0, 1.0],
		]

def matrix_rotate(axis, angle):
	vx	= axis[0]
	vy	= axis[1]
	vz	= axis[2]
	vx2 = vx * vx
	vy2 = vy * vy
	vz2 = vz * vz
	cos = math.cos(angle)
	sin = math.sin(angle)
	co1 = 1.0 - cos
	return [
		[			vx2 * co1 + cos,   vx * vy * co1 + vz * sin,   vz * vx * co1 - vy * sin, 0.0],
		[  vx * vy * co1 - vz * sin, 			vy2 * co1 + cos,   vy * vz * co1 + vx * sin, 0.0],
		[  vz * vx * co1 + vy * sin,   vy * vz * co1 - vx * sin, 			vz2 * co1 + cos, 0.0],
		[0.0, 0.0, 0.0, 1.0],
		]

def matrix_scale(fx, fy, fz):
	return [
		[ fx, 0.0, 0.0, 0.0],
		[0.0,  fy, 0.0, 0.0],
		[0.0, 0.0,	fz, 0.0],
		[0.0, 0.0, 0.0, 1.0],
		]

def point_by_matrix(p, m):
	return [p[0] * m[0][0] + p[1] * m[1][0] + p[2] * m[2][0] + m[3][0],
			p[0] * m[0][1] + p[1] * m[1][1] + p[2] * m[2][1] + m[3][1],
			p[0] * m[0][2] + p[1] * m[1][2] + p[2] * m[2][2] + m[3][2]]

def point_distance(p1, p2):
	return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)

def vector_by_matrix(p, m):
	return [p[0] * m[0][0] + p[1] * m[1][0] + p[2] * m[2][0],
			p[0] * m[0][1] + p[1] * m[1][1] + p[2] * m[2][1],
			p[0] * m[0][2] + p[1] * m[1][2] + p[2] * m[2][2]]

def vector_length(v):
	return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])

def vector_normalize(v):
	l = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
	try:
		return v[0] / l, v[1] / l, v[2] / l
	except:
		return 1, 0, 0

def vector_dotproduct(v1, v2):
	return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def vector_crossproduct(v1, v2):
	return [
		v1[1] * v2[2] - v1[2] * v2[1],
		v1[2] * v2[0] - v1[0] * v2[2],
		v1[0] * v2[1] - v1[1] * v2[0],
		]

def vector_angle(v1, v2):
	s = vector_length(v1) * vector_length(v2)
	f = vector_dotproduct(v1, v2) / s
	if f >=	1.0: return 0.0
	if f <= -1.0: return math.pi / 2.0
	return math.atan(-f / math.sqrt(1.0 - f * f)) + math.pi / 2.0


'''
float trace = 1 + m.M11 + m.M22 + m.M33;
float S = 0;
float X = 0;
float Y = 0;
float Z = 0;
float W = 0;

if (trace > 0.0000001)
{
    S = (float)Math.Sqrt(trace) * 2;
    X = (m.M23 - m.M32) / S;
    Y = (m.M31 - m.M13) / S;
    Z = (m.M12 - m.M21) / S;
    W = 0.25f * S;
}
else
{
    if (m.M11 > m.M22 && m.M11 > m.M33)
    {
        // Column 0:
        S = (float)Math.Sqrt(1.0 + m.M11 - m.M22 - m.M33) * 2;
        X = 0.25f * S;
        Y = (m.M12 + m.M21) / S;
        Z = (m.M31 + m.M13) / S;
        W = (m.M23 - m.M32) / S;
    }
    else if (m.M22 > m.M33)
    {
        // Column 1:
        S = (float)Math.Sqrt(1.0 + m.M22 - m.M11 - m.M33) * 2;
        X = (m.M12 + m.M21) / S;
        Y = 0.25f * S;
        Z = (m.M23 + m.M32) / S;
        W = (m.M31 - m.M13) / S;
    }
    else
    {
        // Column 2:
        S = (float)Math.Sqrt(1.0 + m.M33 - m.M11 - m.M22) * 2;
        X = (m.M31 + m.M13) / S;
        Y = (m.M23 + m.M32) / S;
        Z = 0.25f * S;
        W = (m.M12 - m.M21) / S;
    }
}

return new OpenTK.Quaternion(X, Y, Z, W);
'''