import os
import io
import sys
import gzip
from struct import *

class BinaryReader:
	def __init__(self, data):
		if isinstance(data,str):
			self.base_stream = open(data,'rb')
		else:
			self.base_stream = data

	def tell(self):
		return self.base_stream.tell()

	def seek(self,*args):
		return self.base_stream.seek(*args)

	def Length(self):
		cur_pos = self.base_stream.tell()
		self.base_stream.seek(0,2)
		length = self.base_stream.tell()
		self.base_stream.seek(cur_pos)
		return length

	def setPosition(self,pos):
		self.seek(pos,os.SEEK_SET)

	def unpack(self, fmt, length = 1):
		return unpack(fmt, self.base_stream.read(length))[0]

	def load(self,fmt,length):
		return unpack(fmt, self.base_stream.read(length))

	def skip(self,length):
		self.readBytes(length)

	def readByte(self):
		return self.base_stream.read(1)

	def readBytes(self, length):
		return self.base_stream.read(length)

	def readChar(self):
		return self.unpack('b')

	def readUChar(self):
		return self.unpack('B')

	def readBool(self):
		return self.unpack('?')

	def readInt16(self):
		return self.unpack('h', 2)

	def readUInt16(self):
		return self.unpack('H', 2)

	def readInt32(self):
		return self.unpack('i', 4)

	def readUInt32(self):
		return self.unpack('I', 4)

	def readInt64(self):
		return self.unpack('q', 8)

	def readUInt64(self):
		return self.unpack('Q', 8)

	def readFloat(self):
		return self.unpack('f', 4)

	def readDouble(self):
		return self.unpack('d', 8)

	def readString(self):
		length = self.readUInt16()
		return self.unpack(str(length) + 's', length)

	def readUTF(self):
		leng =  self.unpack('>H',2)
		return self.readBytes(leng).decode('u8')



class BinaryWriter:

	def __init__(self, filename):
		self.base_stream = open(filename,'wb')

	def tell(self):
		return self.base_stream.tell()

	def seek(self,*args):
		return self.base_stream.seek(*args)

	def Length(self):
		cur_pos = self.base_stream.tell()
		self.base_stream.seek(0,2)
		length = self.base_stream.tell()
		self.base_stream.seek(cur_pos)
		return length

	def writeBytes(self, value):
		self.base_stream.write(value)

	def writeChar(self, value):
		self.pack('c', value)

	def writeUChar(self, value):
		self.pack('C', value)

	def writeBool(self, value):
		self.pack('?', value)

	def writeInt16(self, value):
		self.pack('h', value)

	def writeUInt16(self, value):
		self.pack('H', value)

	def writeInt32(self, value):
		self.pack('i', value)

	def writeUInt32(self, value):
		self.pack('I', value)

	def writeInt64(self, value):
		self.pack('q', value)

	def writeUInt64(self, value):
		self.pack('Q', value)

	def writeFloat(self, value):
		self.pack('f', value)

	def writeDouble(self, value):
		self.pack('d', value)

	def writeString(self, value):
		length = len(value)
		self.writeUInt16(length)
		self.pack(str(length) + 's', value)

	def pack(self, fmt, data):
		return self.writeBytes(pack(fmt, data))

	def unpack(self, fmt, length = 1):
		return unpack(fmt, self.base_stream.read(length))[0]

class BigEndianBinaryReader(BinaryReader):

	def readInt16(self):
		return self.unpack('>h', 2)

	def readUInt16(self):
		return self.unpack('>H', 2)

	def readInt32(self):
		return self.unpack('>i', 4)

	def readUInt32(self):
		return self.unpack('>I', 4)

	def readInt64(self):
		return self.unpack('>q', 8)

	def readUInt64(self):
		return self.unpack('>Q', 8)

	def readFloat(self):
		return self.unpack('>f', 4)

	def readDouble(self):
		return self.unpack('>d', 8)

	def readUTF(self):
		leng =  self.unpack('>H',2)
		bytes = self.readBytes(leng)
		return bytes.decode('u8')

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
		length = binaryReader.readInt32()
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

	def __getitem__(self,idx):
		return self.tagList[idx]

	def __len__(self):
		return len(self.tagList)

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

	def __getitem__(self,key):
		if key in self.tagMap:
			tag = self.tagMap[key]
			if isinstance(tag,(NBTTagCompound,NBTTagList)):
				return tag
			elif isinstance(tag, NBTTagByteArray):
				return tag.byteArray
			elif isinstance(tag, NBTTagIntArray):
				return tag.intArray
			else:
				return tag.data
		else:
			raise Exception("DUDE,WHY DO U DO THIS")

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
	def readFromString(cls,data):
		return cls.readFromStream(io.BytesIO(data))

	@classmethod
	def readCompressed(cls,filename):
		return cls.readFromStream(gzip.GzipFile(filename,'rb'))

	@classmethod
	def readFromStream(cls,stream):
		return cls.readNamedTag(BigEndianBinaryReader(stream))

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

if __name__ == '__main__':
	nbt = NBTFactory.readCompressed()
	