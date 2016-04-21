#include "LevelRender.h"

LevelRender::LevelRender(Level* level):
mLevel(level)
{
	mWorldRender = new WorldRender(level,this);
	mFrustum = new Frustum();
	mNewX = mNewY	= mNewZ = 0;
}

LevelRender::~LevelRender()
{
	delete mWorldRender;
	delete mFrustum;
}

void LevelRender::update(float x,float y,float z)
{
	mLastX = mNewX;
	mLastY = mNewY;
	mLastZ = mNewZ;
	mDeltaX = x-mLastX;
	mDeltaY = y-mLastY;
	mDeltaZ = z-mLastZ;
	mNewX = x;
	mNewY = y;
	mNewZ = z;

	mFrustum->update();
	mFrustum->mPosition[0] = x;
	mFrustum->mPosition[1] = y;
	mFrustum->mPosition[2] = z;
	mWorldRender->update();
}

void LevelRender::render(float x,float y,float z)
{
	mWorldRender->render();

	mFrustum->render();
}
