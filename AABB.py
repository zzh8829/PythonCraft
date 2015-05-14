class AABB

	def __init__(self,*args):
		self.minX = 0
		self.minY = 0
		self.minZ = 0
		self.maxX = 0
		self.maxY = 0
		self.maxZ = 0

		if len(args)==6:
			self.setBound(*args)

	def setBound(self,ix,iy,iz,ax,ay,az):
		self.minX = ix
		self.minY = iy
		self.minZ = iz
		self.maxX = ax
		self.maxY = ay
		self.maxZ = az

	def intersect(self,aabb):
		if aabb.maxX > self.minX and aabb.minX < self.maxX:
			if aabb.maxY > self.minY and aabb.minY < self.maxY:
				return aabb.maxZ > self.minZ and aabb.minZ < self.maxZ
			else:
				return False
		else:
			return False



