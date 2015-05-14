#ifndef _SECTIONRENDER_H_
#define _SECTIONRENDER_H_

#include "CommonInc.h"
#include "Section.h"
#include "Level.h"

#include <SDL_opengl.h>
#include <gl/gl.h>
#include <gl/glu.h>

#include "QuadBuilder.h"

#include "math/AABB.h"



class SectionRender
{
public:
	SectionRender(Level* level):
	mLevel(level),
	mSection(0),
	isDirty(true),
	inQueue(false),
	mX(0),
	mY(0),
	mZ(0),
	mDisplayList(0)
	{
		for(int i=0;i!=6;i++)
		{
			mAdjSections[i]=0;
		}

	}

	static const int DELTAFACE[6][3];

	void setSection(Section* section)
	{
		mSection = section;
		isDirty = true;
	}

	void setPosition(int x,int y,int z);
	void update();
	bool shouldRender(int x,int y,int z,int face);

	void render();

	AABB getAABB();

	int mX,mY,mZ;
	Section* mSection;
	Section* mAdjSections[6];
	Level* mLevel;
	int mDisplayList;
	bool isDirty,inQueue;
};

#endif