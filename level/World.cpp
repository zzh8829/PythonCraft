#include "World.h"
#include "NBT.h"

using namespace std;

World::World(string path):
mDirectory(path)
{
}

World::~World()
{
	for(map<Int2,Region*>::iterator it = mRegions.begin();it!=mRegions.end();it++ )
	{
		delete (it->second);
	}
	mRegions.clear();
}

void World::loadWorld()
{
	
}

uint8_t World::getBlockId(int x,int y,int z)
{
	return getChunkData(x>>4,z>>4)->getBlockId(x&15,y,z&15);
}

void World::setBlockId(int x,int y,int z,int id)
{
	int ix = x>>4,iz=z>>4,xx=x&15,zz=z&15;
	if(xx==0)getChunkData(ix-1,iz)->getSection(y>>4)->isDirty = 1;
	if(zz==0)getChunkData(ix,iz-1)->getSection(y>>4)->isDirty = 1;
	if(xx==15)getChunkData(ix+1,iz)->getSection(y>>4)->isDirty = 1;
	if(zz==15)getChunkData(ix,iz+1)->getSection(y>>4)->isDirty = 1;
	getChunkData(ix,iz)->setBlockId(xx,y,zz,id);
}

Region* World::getRegion(Int2 pos)
{
	if (mRegions.find(pos)==mRegions.end())
	{
		ostringstream ss;
		ss << mDirectory << "r." << pos.first << "." << pos.second <<".mca";
		cout << ss.str() << endl;
		mRegions[pos] = new Region(pos,ss.str());
	}
	return mRegions[pos];
}


ChunkData* World::getChunkData(int x,int z)
{
	int rx = x>>5;
	int rz = z>>5;

	Region* region = getRegion(Int2(rx,rz));
	return region->getChunkData(Int2(x-(rx<<5),z-(rz<<5)));
}

void World::deleteRegion(int x,int z)
{
	Int2 pos = Int2(x,z);
	if(mRegions.find(pos)!=mRegions.end())
	{
		delete mRegions[pos];
		mRegions.erase(pos);
	}
}

void World::deleteChunkData(int x,int z)
{
	int rx = x>>5;
	int rz = z>>5;

	Region* region = getRegion(Int2(rx,rz));
	region->deleteChunkData(Int2(x-(rx<<5),z-(rz<<5)));
}

vector< pair<int, int> > World::getLoadedRegions()
{
	vector< pair<int, int> > keys;
	for(map<Int2,Region*>::iterator it = mRegions.begin();it!=mRegions.end();it++ )
	{
		keys.push_back(it->first);
	}
	return keys;
}