#ifndef _SECTION_H_
#define _SECTION_H_

#include "CommonInc.h"
#include "NibbleArray.h"
#include "NBT.h"

class Section
{
public:
	Section(uint8_t y=0);
	~Section();

	void loadFromNBT(NBT::TagCompound* tag);
	uint8_t getBlockId(int x,int y,int z);
	void setBlockId(int x,int y,int z,uint8_t id);
	uint8_t getMetaData(int,int,int);
	void setMetaData(int,int,int,uint8_t);

//private:
	NibbleArray mSkyLight;
	NibbleArray mBlockLight;
	NibbleArray mMetaData;
	uint8_t mBlocks[16*16*16];
	uint8_t mY;
	bool isDirty;
};

#endif