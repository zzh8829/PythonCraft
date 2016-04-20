#ifndef _WORLDRENDER_H_
#define _WORLDRENDER_H_

#include "Level.h"
#include "SectionRender.h"
#include "LevelRender.h"

class LevelRender;
class WorldRender
{
public:
	typedef std::pair<int,int> Int2;

	static const int MAXSIZE;
	static const int MAXHALFSIZE;
	static const int MINSIZE;
	static const int MINHALFSIZE;
	static const int MAXY;
	static const int MAXUPDATE;

	WorldRender(Level* level,LevelRender* levelRender);
	~WorldRender();

	void update();

	void render();

	void shiftEnqueueSections(int,int);
	void enqueueSections();
	void processUpdateQueue();

	void loadSections();

	void setViewDistance(int);

	int mBaseX,mBaseZ;
	int mOrgX,mOrgZ,mOrgY;
	std::vector< std::vector< std::vector<SectionRender*> > > mSectionRenders[2];
	int mSectionRendersIndex;

	std::deque<SectionRender*> mVisibleSectionRenders;
	std::deque<SectionRender*> mUpdateQueue;

	Level* mLevel;
	LevelRender* mLevelRender;

	bool initialized;
	int frame;
	int mViewDistance;
	int mFullDistance;

	int nEnq;

private:
	struct SectionRenderSorter
	{
		int x,y,z;
		SectionRenderSorter(int,int,int);
		int squareDistance(SectionRender* sr);
		bool operator()(SectionRender* a,SectionRender* b);
	};

};


#endif