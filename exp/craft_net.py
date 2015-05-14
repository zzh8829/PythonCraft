from NBT import *
import os

class NibbleArray:

	def __init__(self,size):
		self.Data = None

class Section:
	
	def __init__(self,y):
		self.Y = y

		self.Blocks = [0]*(16*16*16)
		self.Metadata = NibbleArray(16*16*16)
		self.BlockLight = NibbleArray(16*16*16)
		self.SkyLight = NibbleArray(16*16*16)

		self.noAir = 0

	def getBlockId(self,x,y,z):
		return self.Blocks[x + (z * 16) + (y * 16 * 16)]

	def setBlockId(self,x,y,z,Id):
		self.Blocks[x + (z * 16) + (y * 16 * 16)] = Id

	def ProcessSection(self):
		self.Blocks = list(self.Blocks)

class Chunk:
	
	def __init__(self,pos):
		self.sections = [ None for i in range(16)]
		self.postion = pos
		self.biomes = [0] * (16*16)
		self.heightMap = [0] * (16*16)
		self.tileEntities = {}

	def loadFromNBT(self,nbt):
		root = nbt['Level']
		self.Biomes = root['Biomes']
		self.HeightMap = root['HeightMap']
		sections = root['Sections']
		for i in range(len(sections)):
			stag = sections[i]
			y = ord(stag['Y'])
			#print(y)
			section = Section(y)
			
			
			section.Blocks = stag['Blocks']
			section.BlockLight.Data = stag['BlockLight']
			section.SkyLight.Data = stag['SkyLight']
			section.Metadata.Data = stag['Data']
			section.ProcessSection()
			
			self.sections[y] = section
		'''
		var tileEntities = root.Get<NbtList>("TileEntities")
		if (tileEntities != null)
		{
			foreach (var tag in tileEntities)
			{
				Vector3 tilePosition
				var entity = TileEntity.FromNbt(tag as NbtCompound, out tilePosition)
				if (entity != null)
					self.TileEntities.Add(tilePosition, entity)
			}
		}
		return self.
		'''

	def getBlockId(self,x,y,z):
		sec = self.sections[self.getSectionNumber(y)]
		y = self.getPositionInSection(y)
		return sec.getBlockId(x,y,z) if sec else 0

	def setBlockId(self,x,y,z,Id):
		sec = self.sections[self.getSectionNumber(y)]
		y = self.getPositionInSection(y)
		sec.setBlockId(x,y,z,Id)

	def getSectionNumber(self,y):
		return int(y) >> 4

	def getPositionInSection(self,y):
		return int(y) & 15


empty = Chunk((0,0,0))
for i in range(16):
	empty.sections[i] = Section(i)
	empty.sections[i].Blocks = [0]*(16*16*16)

import zlib
class Region:

	def __init__(self,pos,world,path):
		self.chunks = {}
		self.postion = pos 
		self.world = world 
		self.offsets = {}
		self.regionFile = open(os.path.join(path,self.getRegionFile(pos)),'rb')

	@classmethod 
	def getRegionFile(self,pos):
		x = int(pos[0])
		z = int(pos[2])
		return "r.%d.%d.mca"%(x,z)

	def getChunk(self,pos):
		if not pos in self.chunks:
			try:
				offset,length = self.getChunkFromTable(pos)
			except:
				self.chunks[pos] = empty
				print("missing chunk", pos)
				return empty

			self.regionFile.seek(offset)
			reader = BigEndianBinaryReader(self.regionFile)
			length = reader.readInt32()
			format = reader.readByte()
			#print(length)
			#print(format)
			import io
			nbt = NBTFactory.readFromStream(io.BytesIO(zlib.decompress(self.regionFile.read(length-1))))
			
			chunk = Chunk(pos)
			chunk.loadFromNBT(nbt)
			chunk.ParentRegion =self
			self.chunks[pos] = chunk
		return self.chunks[pos]

	def getChunkFromTable(self,pos):
		#print(pos)
		tableOffset = ((int(pos[0]) % 32) + ((int(pos[2]) % 32)*32)) * 4
		self.regionFile.seek(tableOffset)
		reader = BigEndianBinaryReader(self.regionFile)
		#offset = int.from_bytes(reader.readBytes(3), byteorder='big')

		offset = int.from_bytes(reader.readBytes(3),byteorder='big')
		length = ord(reader.readByte())
		

		#print(offset,length)

		if (offset == 0 or length == 0):
			return None
		return (offset*4096,length * 4096)

class World:

	def __init__(self,level,path):
		self.level = level
		self.entityies = []
		self.regions = {}

		self.directory = path

	def getChunk(self,pos):

		x = pos[0]
		z = pos[2]

		rx = x//32
		rz = z//32

		if x<0 : rx -=1
		if z<0 : rz -=1

		rx = x>>5
		rz = z>>5

		region = self.loadRegion((rx,0,rz))
		return region.getChunk((x-(rx<<5),0,z-(rz<<5)))

	def loadRegion(self,pos):
		if not pos in self.regions:
			self.regions[pos] = Region(pos,self,self.directory)
		return self.regions[pos]



def worldToChunkCoord(pos):
	x = int(pos[0])
	y = int(pos[1])
	z = int(pos[2])

	if (y < 0 or y >= 256):
		raise Exception("OUT OF RANGE")

	chunkX = x // 16
	chunkZ = z // 16

	if x<0: chunkX -= 1
	if z<0: chunkZ -= 1

	chunkX = x>>4
	chunkZ = z>>4

	return (chunkX, 0, chunkZ)
class Level:

	def __init__(self,path):
		self.name = ""
		self.time = 0
		self.gameMode = 0
		self.mapFeatures = 0
		self.seed = 0
		self.generatorName = 0
		self.spawnX = 0
		self.spawnY = 0
		self.spawnZ = 0

		self.levelDirectory = path

		self.world = None

		self.loadFromFile()
		chunk = self.world.getChunk(worldToChunkCoord((self.spawnX,self.spawnY,self.spawnZ)))

	def loadFromFile(self):
		levelData = NBTFactory.readCompressed(os.path.join(self.levelDirectory, "level.dat"))
		data = levelData['Data']
		self.name = data['LevelName']
		self.seed = data['RandomSeed']
		self.time = data['Time']
		self.gameMode = data['GameType']
		self.mapFeatures = data['MapFeatures']
		self.generatorName = data['generatorName']

		self.spawnX = data['SpawnX']
		self.spawnY = data['SpawnY']
		self.spawnZ = data['SpawnZ']

		self.world = World(self, os.path.join(self.levelDirectory, "region"))

		

		player = data['Player']

		print(ord(player['Pos'].getId()))

		self.playerPos = player['Pos'][0],player['Pos'][1],player['Pos'][2]

level = Level("saves/Plain")
if __name__ == '__main__':
	level = Level("../saves/Plain")
