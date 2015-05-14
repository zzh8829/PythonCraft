import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
from ZMath import *

class Camera:

	def __init__(self):

		self.maxPitchRate = 5
		self.maxYawRate = 5
		self.maxRollRate = 5

		self.pitchAngle = 0
		self.yawAngle = 0
		self.rollAngle = 0

		self.maxVelocity = 5
		self.forward = 0
		self.strafe = 0
		self.up = 0

		self.pitch = Quaternion()
		self.yaw = Quaternion()
		self.roll = Quaternion()

		self.position = Vector3()
		self.forwardVector = Vector3()
		self.strafeVector = Vector3()
		self.upVector = Vector3()

	def setPosition(self,pos):
		self.position = Vector3(pos)
		self.position.z = -self.position.z

	def setPerspective(self):

		self.pitch = Quaternion(radians(self.pitchAngle),Vector3(1,0,0))
		self.yaw = Quaternion(radians(self.yawAngle),Vector3(0,1,0))
		self.roll = Quaternion(radians(self.rollAngle),Vector3(0,0,1))

		quat = self.pitch*self.yaw*self.roll


		#glRotated(degrees(quat.x), 1.0, 0.0, 0.0);
		#glRotated(degrees(quat.y), 0.0, 1.0, 0.0);
		#glRotated(degrees(quat.z), 0.0, 0.0, 1.0);


		self.viewMatrix = quat.toMatrix()
		glMultMatrixf(self.viewMatrix)

		quat = self.yaw*self.pitch*self.roll
		mat = quat.toMatrix()

		self.strafeVector.x = mat[0][0]
		self.strafeVector.y = mat[0][1]
		self.strafeVector.z = mat[0][2]

		self.forwardVector.x = mat[2][0]
		self.forwardVector.y = mat[2][1]
		self.forwardVector.z = mat[2][2]

		#self.upVector.x = mat[1][0]
		#self.upVector.y = mat[1][1]
		#self.upVector.z = mat[1][2]
		self.upVector.y = 1

		self.strafeVector *= self.strafe
		self.forwardVector *= self.forward
		self.upVector *= self.up

		self.position += self.forwardVector + self.strafeVector + self.upVector
		#self.position.z = -self.position.z

		glTranslatef(-self.position.x,-self.position.y,self.position.z)


	def Roll(self,angle):
		if abs(angle) < abs(self.maxRollRate):
			self.rollAngle += angle
		else:
			if angle < 0:
				self.rollAngle -= self.maxRollRate
			else:
				self.rollAngle += self.maxRollRate

		self.rollAngle%=360

	def Yaw(self,angle):
		if abs(angle) < abs(self.maxYawRate):
			self.yawAngle += angle
		else:
			if angle < 0:
				self.yawAngle -= self.maxYawRate
			else:
				self.yawAngle += self.maxYawRate

		self.yawAngle%=360

	def Pitch(self,angle):
		if abs(angle) < abs(self.maxPitchRate):
			self.pitchAngle += angle
		else:
			if angle < 0:
				self.pitchAngle -= self.maxPitchRate
			else:
				self.pitchAngle += self.maxPitchRate

		self.pitchAngle%=360

	def MoveZ(self,velocity):
		if abs(velocity) < abs(self.maxVelocity):
			self.forward = velocity
		else:
			if velocity<0:
				self.forward = -self.maxVelocity
			else:
				self.forward = self.maxVelocity

	def MoveX(self,velocity):
		if abs(velocity) < abs(self.maxVelocity):
			self.strafe = velocity
		else:
			if velocity<0:
				self.strafe = -self.maxVelocity
			else:
				self.strafe = self.maxVelocity

	def MoveY(self,velocity):
		if abs(velocity) < abs(self.maxVelocity):
			self.up = velocity
		else:
			if velocity<0:
				self.up = -self.maxVelocity
			else:
				self.up = self.maxVelocity

	def getMouseRay(self,x,y):
		model = glGetDoublev(GL_MODELVIEW_MATRIX)
		proj = glGetDoublev(GL_PROJECTION_MATRIX)
		vp = glGetIntegerv(GL_VIEWPORT)
		near = gluUnProject(x,vp[3]-y,0,model,proj,vp)
		far = gluUnProject(x,vp[3]-y,1,model,proj,vp)
		return Vector3(near),Vector3(far)


	def reset(self):
		self.__init__()







