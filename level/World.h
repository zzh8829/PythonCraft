#ifndef _WORLD_H_
#define _WORLD_H_

#include "CommonInc.h"
#include "Region.h"
#include "ChunkData.h"

class World
{
public:
	typedef std::pair<int,int> Int2;

	World(std::string path);
	virtual ~World();
	void loadWorld();

	Region* getRegion(Int2 pos);
	ChunkData* getChunkData(int x,int z);
	uint8_t getBlockId(int x,int y,int z);
	void setBlockId(int x,int y,int z,int id);
	void deleteRegion(int x,int z);
	void deleteChunkData(int x,int z);
	std::vector<Int2> getLoadedRegions();

private:
	std::string mDirectory;
	std::map<Int2,Region*> mRegions;
};

#endif