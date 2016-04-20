#ifndef _CHUNK_DATA_H_
#define _CHUNK_DATA_H_

#include "Section.h"
#include "NBT.h"

class ChunkData
{
public:
	typedef std::pair<int,int> Int2;
	ChunkData(Int2 pos);
	ChunkData();
	virtual ~ChunkData();

	void loadFromNBT(NBT::TagCompound* nbt);

	uint8_t getBlockId(int x,int y,int z);
	Section* getSection(int y);

	void setBlockId(int x,int y,int z,uint8_t id);



private:
	Section mSections[16];
	Int2 mPos;

};

#endif