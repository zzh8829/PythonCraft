#include "Region.h"
#include "Endian.h"
using namespace std;

Region::Region(Int2 pos,string path):
mPos(pos),
mRegionFile(path.c_str(),ios_base::in|ios_base::binary)
{
	if(!mRegionFile.is_open())
	{
		for(int i=0;i!=32;i++)
		{
			for(int j=0;j!=32;j++)
			{
				mChunks[Int2(i,j)] = new ChunkData(Int2(i,j));
			}
		}
	}
	/*
	string str;
	while(getline(mRegionFile,str))
	{
		cout << str << endl;
	}
	*/
}
Region::~Region()
{
	for(map<Int2,ChunkData*>::iterator it=mChunks.begin();it!=mChunks.end();it++)
	{
		if(it->second) 
			delete (it->second);
	}
	mChunks.clear();
	if(mRegionFile.is_open())
	{
		mRegionFile.close();
	}
}

ChunkData* Region::getChunkData(Int2 pos)
{
	if(mChunks.find(pos)==mChunks.end())
	{
		int offset = getOffset(pos);
		//cout << offset << endl;
		if(offset==-1)
		{
			mChunks[pos] = new ChunkData(pos);
			cout << "Missing Chunk " << pos.first <<" " << pos.second << endl;
			return mChunks[pos];
		}
		mRegionFile.seekg(offset,mRegionFile.beg);
		int length = NBT::ReadSwap<int32_t>(mRegionFile);
		uint8_t format = NBT::Read<uint8_t>(mRegionFile);
		NBT::TagCompound* tag = NBT::ReadNBTFromZlibStream(mRegionFile);
		ChunkData* chunk = new ChunkData(pos);
		chunk->loadFromNBT(tag);
		mChunks[pos] = chunk;
		delete tag;
	}
	return mChunks[pos];
}

void Region::deleteChunkData(Int2 pos)
{
	if(mChunks.find(pos)!=mChunks.end())
	{
		delete mChunks[pos];
		mChunks.erase(pos);
	}
}

int Region::getOffset(Int2 pos)
{
	if(mOffsets.find(pos)==mOffsets.end())
	{
		int position = (pos.first%32 + (pos.second%32) * 32) * 4;
		mRegionFile.seekg(position,mRegionFile.beg);
		uint32_t offset = (NBT::ReadSwap<uint32_t>(mRegionFile) >>8 ) << 12;
		if(offset == 0) offset = -1;
		mOffsets[pos] = offset;
	}
	return mOffsets[pos];
}