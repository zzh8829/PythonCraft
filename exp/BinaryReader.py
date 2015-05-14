import os
import sys
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

class InibinBinaryReader(BinaryReader):
	def __init__(self,base_stream):
		super().__init__(base_stream)

	def readShort(self):
		return self.ReadInt16()

	def readSegmentKeys(self):
		count = self.ReadShort()
		print ("segment key count", count)
		if (count < 0):
			return None
		result = []
		for i in range(count):
			result.append(self.ReadInt32())
			print ("key[" + str(i) + "]", result[i])
		return result

	def readNullTerminatedString(self,atOffset):
		oldPos = self.tell()
		self.seek(atOffset, 0)
		sb = ""
		c = self.ReadChar()
		while c>0:
			sb+=chr(c)
			c = self.ReadChar()
		self.seek(oldPos,0)
		return sb

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