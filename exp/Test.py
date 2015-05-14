import pygame
import OpenGL
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Tessellator:

	convertQuadsToTriangles = False
	tryVBO = False

	def __init__(self,bufsize = 2097152 ):
		self.bufferSize = bufsize
		self.byteBuffer = np.array(range(bufsize*4),dtype = 'b')
		self.rawBuffer = np.array(range(bufsize),dtype = 'f')

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



class Block:

	blocksList = ['air','dirt']

	def __init__(self):
		pass

	def hasComparatorInputOverride():
		return False

class Chunk:

	def __init__(self,world,x,z):
		self.isChunkLoaded  = False

		#self.storageArrays = new ExtendedBlockStorage[16]
		self.blockBiomeArray = [-1 for i in range(256)]
		self.precipitationHeightMap = [-999 for i in range(256)]
		#self.updateSkylightColumns = new boolean[256]
		self.isGapLightingUpdated = False
		#self.chunkTileEntityMap = new HashMap()
		self.isTerrainPopulated = False
		self.isModified = False
		self.hasEntities = False
		self.lastSaveTime = 0
		self.sendUpdates = False
		self.heightMapMinimum = 0
		self.queuedLightChecks = 4096
		self.field_76653_p = False
		self.entityLists = [ [] for i in range(16)]
		self.worldObj = world
		self.xPosition = x
		self.zPosition = z
		self.heightMap = [0 for i in range(256)]

	def getBlockId(self,x,y,z):
		print(x,y,z)
		return 1

class EmptyChunk(Chunk):

	def __init__(self,world,x,z):
		super().__init__(world,x,z)

class ChunkPosition:

	def __init__(self,x,y,z):
		self.x = z
		self.y = y
		self.z = z

class ChunkCoordIntPair:

	def __init__(self,x,z):
		self.chunkX = x
		self.chunkZ = z

	@staticmethod
	def chunkXZ2Int(x,z):
		return (x & 4294967295) | (z & 4294967295) << 32

	def getCenterXPosition(self):
		return (self.chunkX << 4) + 8

	def getCenterZPosition(self):
		return (self.chunkZ << 4) + 8

	def getCenterPosition(self,y):
		return ChunkPosition(self.getCenterXPosition(),y,self.getCenterZPosition())

	def __str__(self):
		return '[%d, %d]'%(self,chunkX,self.chunkZ)

class ChunkProviderClient:

	def __init__(self,world):

		self.blankChunk = EmptyChunk(world,0,0)
		self.worldObj = world

		self.chunkMapping = {}
		self.chunkListing = []

	def chunkExists(x,z):
		return True

	def loadChunk(self,x,z):
		chunk = Chunk(self.worldObj,x,z)
		self.chunkMapping[ChunkCoordIntPair.chunkXZ2Int(x,z)] = chunk
		chunk.isChunkLoaded =True
		return chunk

	def provideChunk(self,x,z):
		try:
			chunk = self.chunkMapping[ChunkCoordIntPair.chunkXZ2Int(x,z)]
			return chunk
		except:
			return self.blankChunk

class ChunkCoordinates:

	def __init__(self,x=0,y=0,z=0):
		self.posX = x
		self.posY = y
		self.posZ = z

class World:

	def __init__(self,worldInfo):
		self.isRemote = False
		self.chunkProvider = ChunkProviderClient(self)
		self.worldInfo = worldInfo

	def getBlockId(self,x,y,z):
		if x >= -30000000 and z >= -30000000 and x < 30000000 and z < 30000000:
			if y < 0 or y>256:
				return 0
			else:
				chunk = self.getChunkFromChunkCoords(x>>4,z>>4)
				return chunk.getBlockId(x&15 , y, z&15)
		else:
			return 0

	def getChunkFromBlockCoords(self,x,z):
		return self.getChunkFromChunkCoords(x>>4,z>>4)

	def getChunkFromChunkCoords(self,x,z):
		print(x,z)
		return EmptyChunk(self,x,z)

	def isAirBlock(self,x,y,z):
		return self.getBlockId(x,y,z) == 0

	def blockExists(self,x,y,z):
		if 0 <= y < 256:
			return self.chunkExists(x>>4,z>>4)
		else:
			return False

	def setBlock(self,x,y,z,blockId,metadata=0,flags=3):
		if x >= -30000000 and z >= -30000000 and x < 30000000 and z < 30000000:
			if y < 0 or y>256:
				return 0
			else:
				chunk = self.getChunkFromChunkCoords(x>>4,z>>4)
				ID = 0

				if (flags&1) !=0:
					ID = chunk.getBlockId(x&15,y,z&15)

				result = chunk.setBlockIDWithMetadata(x&15,y,z&15,blockId,metadata)
				self.updateAllLightTypes(x,y,z)

				if result == True:
					if (flags&2)!=0 and (not self.isRemote or (flags&4)==0) :
						self.markBlockForUpdate(x,y,z)

					if not self.isRemote and (flags&1) != 0:
						self.notifyBlockChange(x,y,z,ID)
						block = Block.blocksList[blockId]

						if block and block.hasComparatorInputOverride():
							pass
							#self.function(x,y,z,blockId)

				return result
		else:
			return 0


	def updateAllLightTypes(self,x,y,z):
		pass

	def markBlockForUpdate(self,x,y,z):
		pass

	def isAABBNonEmpty(self,aabb):
		minx = int(aabb.minX)
		maxx = int(aabb.maxX + 1)
		miny = int(aabb.minY)
		maxy = int(aabb.maxY + 1)
		minz = int(aabb.minZ)
		maxz = int(aabb.maxZ + 1)
		if aabb.minX < 0:
			minx -= 1
		if aabb.minY < 0:
			miny -= 1
		if aabb.minZ < 0:
			minz -= 1
		for x in range(minx,maxx):
			for y in range(miny,maxy):
				for z in range(minz,maxz):
					try:
						block = Block.blocksList[self.getBlockId(x, y, z)]
						if block:
							return True
					except:
						pass
		return False

	def getSpawnPoint():
		return ChunkCoordinates(self.worldInfo.spawnX,self.worldInfo.spawnY, self.worldInfo.spawnZ)

class NBTBase:

	def __init__(self,name):
		self.name = name

	def setName(self,name = ""):
		self.name = name

	def getName(self):
		return self.name if self.name else ""

class NBTTagEnd(NBTBase):

	def __init__(self,name = ""):
		super().__init__(name)

	def __str__(self):
		return 'END'

	def getId(self):
		return '\x00'

class NBTTagByte(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

	def load(self,binaryReader):
		self.data = binaryReader.readByte()

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x01'

	def __str__(self):
		return str(self.data)

class NBTTagShort(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

	def load(self,binaryReader):
		self.data = binaryReader.readInt16()

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x02'

	def __str__(self):
		return str(self.data)

class NBTTagInt(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

	def load(self,binaryReader):
		self.data = binaryReader.readInt32()

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x03'

	def __str__(self):
		return str(self.data)

class NBTTagLong(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

	def load(self,binaryReader):
		self.data = binaryReader.readInt64()

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x04'

	def __str__(self):
		return str(self.data)

class NBTTagFloat(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

	def load(self,binaryReader):
		self.data = binaryReader.readFloat()

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x05'

	def __str__(self):
		return str(self.data)

class NBTTagDouble(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

	def load(self,binaryReader):
		self.data = binaryReader.readDouble()

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x06'

	def __str__(self):
		return str(self.data)

class NBTTagByteArray(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data
		self.byteArray = b""

	def load(self,binaryReader):
		length = binaryReader.readInt()
		self.byteArray = binaryReader.readBytes(length)

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x07'

	def __str__(self):
		return str(self.data)

class NBTTagString(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

	def load(self,binaryReader):
		self.data = binaryReader.readUTF()

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x08'

	def __str__(self):
		return str(self.data)

class NBTTagList(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data

		self.tagList = []
		self.tagType = '\x00'

	def load(self,binaryReader):
		self.tagType = binaryReader.readByte()
		length = binaryReader.readInt32()
		self.tagList = []
		for i in range(length):
			tag = NBTFactory.newTag(self.tagType,"")
			tag.load(binaryReader)
			self.tagList.append(tag)

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x09'

	def __str__(self):
		return str(self.data)

class NBTTagCompound(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data
		self.tagMap = {}

	def load(self,binaryReader):
		self.tagMap = {}

		while True:
			tag = NBTFactory.readNamedTag(binaryReader)
			if ord(tag.getId()) == 0:
				break
			self.tagMap[tag.getName()] = tag

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x0a'

	def getCompoundTag(self,name):
		try: return self.tagMap[name]
		except: return NBTTagCompound(name)
	def getByte (self,name):
		try: return self.tagMap[name].data
		except: return b""
	def getShort(self,name):
		try: return self.tagMap[name].data
		except: return 0
	def getInteger(self,name):
		try: return self.tagMap[name].data
		except: return 0
	def getLong(self,name):
		try: return self.tagMap[name].data
		except: return 0
	def getFloat(self,name):
		try: return self.tagMap[name].data
		except: return 0.0
	def getDouble(self,name):
		try: return self.tagMap[name].data
		except: return 0.0
	def getString(self,name):
		try: return self.tagMap[name].data
		except: return ""
	def getByteArray(self,name):
		try: return self.tagMap[name].byteArray
		except: return b""
	def getIntArray(self,name):
		try: return self.tagMap[name].intArray
		except: return []
	def getTagList (self,name):
		try: return self.tagMap[name]
		except: return NBTTagList(name)
	def getBoolean(self,name):
		try: return ord(self.getByte(name)) != 0
		except: return False

	def hasKey(self,key):
		return key in self.tagMap

	def __str__(self):
		return str(self.data)

class NBTTagIntArray(NBTBase):

	def __init__(self,name = "", data = None):
		super().__init__(name)
		self.data = data
		self.intArray = []

	def load(self,binaryReader):
		length = binaryReader.readInt32()
		self.intArray = []
		for i in range(length):
			self.intArray.append(binaryReader.readInt32())

	def write(self,binaryWriter):
		binaryWriter.write(self.data)

	def getId(self):
		return '\x0b'

	def __str__(self):
		return str(self.data)

class NBTFactory:

	TAGCLASS = 	[
		NBTTagEnd,
		NBTTagByte,
		NBTTagShort,
		NBTTagInt,
		NBTTagLong,
		NBTTagFloat,
		NBTTagDouble,
		NBTTagByteArray,
		NBTTagString,
		NBTTagList,
		NBTTagCompound,
		NBTTagIntArray
	]
	TAGNAME = [
		"TAG_End",
		"TAG_Byte",
		"TAG_Short",
		"TAG_Int",
		"TAG_Long",
		"TAG_Float",
		"TAG_Double",
		"TAG_Byte_Array",
		"TAG_String",
		"TAG_List",
		"TAG_Compound",
		"TAG_Int_Array"
	]

	@classmethod
	def readNamedTag(cls,binaryReader):
		typ = binaryReader.readByte()
		if ord(typ) == 0:
			return NBTTagEnd()
		else:
			val = binaryReader.readUTF()
			tag = cls.newTag(typ,val)
			tag.load(binaryReader)
			return tag

	@classmethod
	def newTag(cls,typ,val):
		return cls.TAGCLASS[ord(typ)](val)

	@classmethod
	def getTagName(cls,typ):
		return cls.TAGNAME[ord(typ)]


from BinaryReader import *
import gzip
def readCompressed(filename):
	stream = BigEndianBinaryReader(gzip.GzipFile(filename,'rb'))
	nbtbase = NBTFactory.readNamedTag(stream)
	return nbtbase


class WorldType:

	worldTypes = [ 0 for i in range(16)]

	def __init__(self,typeId,name):
		self.worldType = name
		self.worldTypeId = typeId
		self.worldTypes[typeId] = self

	@classmethod
	def parseWorldType(cls,name):
		for t in cls.worldTypes:
			if t and name.lower() == t:
				return t

WorldType.DEFAULT = WorldType(0,"default")
WorldType.FLAT = WorldType(1,"flat")
WorldType.LARGE_BIOMES = WorldType(2,"large_biomes")
WorldType.DEFAULT_1_1 = WorldType(8,"default_1_1")

class WorldInfo:

	def __init__(self,*args):
		self.randomSeed = 0
		self.terrainType = WorldType.DEFAULT
		self.generatorOptions = ""

		self.spawnX = 0
		self.spawnY = 0
		self.spawnZ = 0

		self.totalTime = 0
		self.worldTime = 0
		self.lastTimePlayed = 0
		self.sizeOnDisk = 0
		self.playerTag = None
		self.dimension = 0
		self.levelName = 0
		self.saveVersion = 0

		self.raining = False
		self.rainTime = 0
		self.thundering = False
		self.thunderTime = 0

		self.theGameType = None
		self.mapFeaturesEnabled = False

		self.hardcore = False
		self.allowCommands = False
		self.initialized = False

		self.theGameRules = None

		if len(args)==1:
			if isinstance(args[0],NBTBase):
				tag = args[0]
				self.randomSeed = tag.getLong("RandomSeed")
				if(tag.hasKey("generatorName")):
					name = tag.getString("generatorName")
					self.terrainType = WorldType.parseWorldType(name)

					if self.terrainType == None:
						self.terrainType = WorldType.DEFAULT
					elif 0:
						pass

					self.generatorOptions = tag.getString("generatorOptions")

				self.theGameType = tag.getInteger("GameType")

				self.spawnX = tag.getInteger('SpawnX')
				self.spawnY = tag.getInteger('SpawnY')
				self.spawnZ = tag.getInteger('SpawnZ')
				self.totalTime = tag.getLong('Time')
				self.worldTime = tag.getLong('DayTime')

				self.lastTimePlayed = tag.getLong("LastPlayed")
				self.sizeOnDisk = tag.getLong("SizeOnDisk")
				self.levelName = tag.getString("LevelName")
				self.saveVersion = tag.getInteger("version")
				self.rainTime = tag.getInteger("rainTime")
				self.raining = tag.getBoolean("raining")
				self.thunderTime = tag.getInteger("thunderTime")
				self.thundering = tag.getBoolean("thundering")
				self.hardcore = tag.getBoolean("hardcore")

				self.playerTag = tag.getCompoundTag("Player")
				self.dimension = self.playerTag.getInteger('Dimension')

	def getSaveVersion(self):
		return self.saveVersion

	def getWorldName(self):
		return self.levelName


import os
import numpy as np

import struct
import zlib

class RegionFile:

	SECTOR_BYTES = 4096
	SECTOR_INTS = SECTOR_BYTES / 4
	CHUNK_HEADER_SIZE = 5
	VERSION_GZIP = 1
	VERSION_DEFLATE = 2

	def __init__(self,folder,x,z):
		self.filename = os.path.join(folder,"r.%d.%d.mca"%(x,z))
		f = open(self.filename,'rb')
		filesize = os.path.getsize(self.filename)
		if filesize & 0xfff:
			filesize = (filesize|0xfff)+1
			f.truncate(filesize)

		f.seek(0)
		offsetsData = f.read(self.SECTOR_BYTES)
		modTimesData = f.read(self.SECTOR_BYTES)

		#print(offsetsData)

		self.freeSectors = [True] * (filesize // self.SECTOR_BYTES)
		self.freeSectors[0:2] = False, False

		self.offsets = np.fromstring(offsetsData, dtype='>u4')
		self.modTimes = np.fromstring(modTimesData, dtype='>u4')

		print(self.offsets)

		needsRepair = False
		for offset in self.offsets:
			sector = offset >> 8
			count = offset & 0xff

			for i in range(sector, sector + count):
				if i >= len(self.freeSectors):
					# raise RegionMalformed("Region file offset table points to sector {0} (past the end of the file)".format(i))
					print( "Region file offset table points to sector {0} (past the end of the file)".format(i))
					needsRepair = True
					break
				if self.freeSectors[i] is False:
					needsRepair = True
				self.freeSectors[i] = False

	def readChunk(self,x,z):
		x &= 0x1f
		z &= 0x1f
		offset = self.getOffset(x, z)

		sectorStart = offset >> 8
		numSectors = offset & 0xff

		f = open(self.filename,'rb')
		f.seek(sectorStart * self.SECTOR_BYTES)
		data = f.read(numSectors * self.SECTOR_BYTES)



		length = struct.unpack_from(">I", data)[0]
		format = struct.unpack_from("B", data, 4)[0]
		data = data[5:length + 5]

		return zlib.decrompress(data)

	def getOffset(self, cx, cz):
		cx &= 0x1f
		cz &= 0x1f
		return self.offsets[cx + cz * 32]



class AnvilSaveLoader:

	def __init__(self,folder,name):
		self.directory = folder
		self.worldname = name
		self.worldDirectory = os.path.join(folder,name)
		self.playerDirectory = os.path.join(self.worldDirectory,'players')
		self.mapDataDirectory = os.path.join(self.worldDirectory,'data')
		self.saveDirectoryName = name

		self.regionDirectory = os.path.join(self.worldDirectory,'region')

		self.regionFiles = {}

		self.chunks = {}

	def getWorldInfo(self):
		folder = os.path.join(self.directory,self.worldname)
		data = os.path.join(folder,'level.dat')

		cst = readCompressed(data)
		return WorldInfo(cst.getCompoundTag('Data'))

	def getRegionForChunk(self,x,z):
		return self.getRegionFile(x>>5,y>>5)

	def getRegionFile(self,x,z):
		if (x,z) not in self.regionFiles:
			regionFile = RegionFile(self.regionDirectory,x,z)
			self.regionFiles[x,z] = regionFile
		return self.regionFiles[x,z]

	def getChunk(self,x,z):
		if not (x,z) in self.chunks:
			global chunkLoader
			self.chunks[x,z] = chunkLoader.loadChunk(x,z)
		return self.chunks[x,z]

	def readChunkStream(self,x,z):
		return self.getRegionFile(x,z).readChunk(x,z)


class AnvilChunkLoader:

	def __init__(self,world,saveloader):
		self.saveLoader = saveloader
		self.worldObj = world

	def loadChunk(self,x,z):
		pos = ChunkCoordIntPair(x,z)

		stream = self.saveLoader.readChunkStream(x,z)
		tag = NBTFactory.readNamedTag(BigEndianBinaryReader(stream))

		chunk = self.readChunkFromNBT(world,tag)
		if not chunk.isAtLocation(x,z):
			tag.setInteger('xPos',x)
			tag.setInteger('yPos',y)
			chunk = self.readChunkFromNBT(world,tag)

		return chunk

	def readChunkFromNBT(self,world,tag):
		x = tag.getInteger("xPos")
		z = tag.getInteger("zPos")
		chunk = Chunk(world, x, z)
		chunk.heightMap = tag.getIntArray("HeightMap")
		chunk.isTerrainPopulated = tag.getBoolean("TerrainPopulated")
		sections = tag.getTagList("Sections")
		length = 16
		extBlockStorage = [ None for i in range(length)]
		hasSky = not world.provider.hasNoSky

		'''

		for i in range(sections.tagCount()):
			stag = sections.tagAt(i)
			Yval = stag.getByte("Y")
			ExtendedBlockStorage blockStorage = new ExtendedBlockStorage(Yval << 4, hasSky)
			blockStorage.setBlockLSBArray(stag.getByteArray("Blocks"))

			if (stag.hasKey("Add")):
				blockStorage.setBlockMSBArray(new NibbleArray(stag.getByteArray("Add"), 4))

			blockStorage.setBlockMetadataArray(new NibbleArray(stag.getByteArray("Data"), 4))
			blockStorage.setBlocklightArray(new NibbleArray(stag.getByteArray("BlockLight"), 4))

			if (hasSky):
				blockStorage.setSkylightArray(new NibbleArray(stag.getByteArray("SkyLight"), 4))

			blockStorage.removeInvalidBlocks()
			extBlockStorage[Yval] = blockStorage

		chunk.setStorageArrays(extBlockStorage)

		if (tag.hasKey("Biomes")):
			chunk.setBiomeArray(tag.getByteArray("Biomes"))
		'''

		chunk.hasEntities = False

		return chunk

if __name__ == '__main__':

	#world = World()
	#world.getBlockId(100,100,100)

	loader = AnvilSaveLoader('../saves/','Plain')
	info = loader.getWorldInfo()

	world = World(info)

	chunkLoader = AnvilChunkLoader(world,loader)

	def loadChunk(x,z):
		#hashcode = ChunkCoordinates.chunkXZ2Int(x,z)
		chunk = chunkLoader.loadChunk(world,x,z)

	print(info.randomSeed)