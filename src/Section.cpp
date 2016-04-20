#include "Section.h"
#include "NibbleArray.h"
using namespace std;
Section::Section(uint8_t y):
mSkyLight(16*16*16),
mBlockLight(16*16*16),
mMetaData(16*16*16),
mY(y),
isDirty(true)
{
	memset(mBlocks,0,sizeof(uint8_t)*16*16*16);
}

Section::~Section()
{
}

void Section::loadFromNBT(NBT::TagCompound* tag)
{
	mY = tag->getByte("Y");

	vector<uint8_t> blocks = tag->getByteArray("Blocks");
	copy(blocks.begin(),blocks.end(),mBlocks);

	mMetaData.setData(tag->getByteArray("Data"));
	mSkyLight.setData(tag->getByteArray("SkyLight"));
	mBlockLight.setData(tag->getByteArray("BlockLight"));
}

uint8_t Section::getBlockId(int x,int y,int z)
{
	if(y<0 || y >= 256 || x<0 || z< 0|| x>=256 || z>=256) return 0;
	return mBlocks[x+(z+y*16)*16];
}

uint8_t Section::getMetaData(int x,int y,int z)
{
	return mMetaData.getAt(x,y,z);
}

void Section::setBlockId(int x,int y,int z,uint8_t id)
{
	mBlocks[x+(z+y*16)*16] = id;
}

void Section::setMetaData(int x,int y,int z,uint8_t data)
{
	mMetaData.setAt(x,y,z,data);
}