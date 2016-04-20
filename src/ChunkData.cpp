#include "ChunkData.h"

ChunkData::ChunkData(Int2 pos):
mPos(pos)
{
}

ChunkData::ChunkData():
mPos(Int2(0,0))
{
}


ChunkData::~ChunkData()
{
}

uint8_t ChunkData::getBlockId(int x,int y,int z)
{
	return mSections[y>>4].getBlockId(x,y&15,z);
}

Section* ChunkData::getSection(int y)
{
	return &mSections[y];
}


void ChunkData::setBlockId(int x,int y,int z,uint8_t id)
{
	int idx = y>>4,yy=y&15;
	if(yy==0 && idx>0)
	{
		mSections[idx-1].isDirty = 1;
	} else if(yy==15 && idx < 16)
	{
		mSections[idx+1].isDirty = 1;
	}
	mSections[idx].isDirty = 1;
	return mSections[idx].setBlockId(x,yy,z,id);
}

void ChunkData::loadFromNBT(NBT::TagCompound* nbt)
{
	NBT::TagCompound* root = nbt->getCompound("Level");
	NBT::TagList* sections = root->getList("Sections");
	for(int i=0;i!=sections->size();i++)
	{
		mSections[i].loadFromNBT(sections->getCompound(i));
	}
}