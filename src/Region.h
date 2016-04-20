#ifndef _REGION_H_
#define _REGION_H_

#include "CommonInc.h"
#include "ChunkData.h"

class Region
{
public:
	typedef std::pair<int,int> Int2;
	Region(Int2 pos,std::string path);
	virtual ~Region();
	ChunkData* getChunkData(Int2 pos);
	void deleteChunkData(Int2 pos);
	int getOffset(Int2 pos);

private:
	std::map<Int2,ChunkData*> mChunks;
	std::map<Int2,int> mOffsets;
	std::ifstream mRegionFile;
	Int2 mPos;
};

#endif