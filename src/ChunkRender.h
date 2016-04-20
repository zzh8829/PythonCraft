#ifndef _CHUNK_RENDER_H_
#define _CHUNK_RENDER_H_

#if 0
#include "CommonInc.h"
#include <SDL_opengl.h>
#include <gl/gl.h>
#include <gl/glu.h>
#include "SectionRender.h"

class ChunkRender
{
public:
	static const int HEIGHT = 16;

	ChunkRender(Level* level):mLevel(level),isDirty(true)
	{
		for(int i=0;i!=HEIGHT;i++)
		{
			mSectionRenders.push_back(new SectionRender(this));
		}
	}

	~ChunkRender()
	{
		for(int i=0;i!=HEIGHT;i++)
		{
			delete mSectionRenders[i];
		}
		mSectionRenders.clear();
	}

	void setPosition(int x,int z)
	{
		mChunkData = mLevel->getWorld()->getChunkData(x,z);

		for(int i=0;i!=HEIGHT;i++)
		{
			mSectionRenders[i]->setSection(mChunkData->getSection(i));
		}
		mX = x;
		mZ = z;
	}

	void update()
	{
		for(int i=0;i!=HEIGHT;i++) if(mSectionRenders[i].isDirty)
		{
			mSectionRenders[i]->update();
		}
	}

	void render()
	{
		for(int i=0;i!=HEIGHT;i++)
		{
			glTranslatef(0,0,0)
			mSectionRenders[i]->render();
		}
	}

	void setDirty()
	{
		for(int i=0;i!=HEIGHT;i++)
		{
			mSectionRenders[i]->isDirty = true;
		}
	}
	void setDirty(int y)
	{
		mSectionRenders[y]->isDirty = true;
	}

private:
	ChunkData* mChunkData;
	Level* mLevel;

	bool isDirty;

	int mX,mZ;

	std::vector< SectionRender* > mSectionRenders;

};
#endif

#endif