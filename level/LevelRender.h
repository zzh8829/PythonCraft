#ifndef _LEVELRENDER_H_
#define _LEVELRENDER_H_

#include "CommonInc.h"
#include "Level.h"

//#include "ChunkRender.h"
#include "WorldRender.h"
#include "Frustum.h"

class WorldRender;
class LevelRender
{
public:
	LevelRender(Level* level);
	~LevelRender();

	void update(float x,float y,float z);
	void render(float x,float y,float z);
	WorldRender* getWorldRender(){return mWorldRender;}

	float mLastX,mLastY,mLastZ;
	float mNewX,mNewY,mNewZ;
	float mDeltaX,mDeltaY,mDeltaZ;
	Level* mLevel;
	WorldRender* mWorldRender;
	Frustum* mFrustum;

};

#endif