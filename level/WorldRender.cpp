#include "WorldRender.h"
#include "TextureManager.h"
#include "math/sort.h"
using namespace std;

WorldRender::WorldRender(Level* level,LevelRender* levelRender):
mLevel(level),
mLevelRender(levelRender)
{
	mSectionRendersIndex = 0;
	for(int i=0;i!=MAXSIZE;i++)
	{
		vector< vector<SectionRender*> > vvc;
		for(int j=0;j!=MAXSIZE;j++)
		{
			vector<SectionRender*> vc;
			for(int k=0;k!=MAXY;k++)
			{
				vc.push_back(new SectionRender(mLevel));
			}
			vvc.push_back(vc);
		}
		mSectionRenders[0].push_back(vvc);
	}
	mSectionRenders[1] = mSectionRenders[0];

	initialized = 0;
	setViewDistance(16);
	frame = 0;
}
WorldRender::~WorldRender()
{
	for(int i=0;i!=MAXSIZE;i++)
	{
		for(int j=0;j!=MAXSIZE;j++)
		{
			for(int k=0;k!=MAXY;k++)
			{
				delete mSectionRenders[mSectionRendersIndex][i][j][k];
			}
		}
	}
	mSectionRenders[0].clear();
	mSectionRenders[1].clear();
}

void WorldRender::setViewDistance(int v)
{
	mViewDistance = max(min(v,MAXHALFSIZE),MINHALFSIZE);
	mFullDistance = mViewDistance*2+1;
}

void WorldRender::update()
{
	int X = int(floor(mLevelRender->mNewX)) >> 4;
	int Z = int(floor(mLevelRender->mNewZ)) >> 4;
	int Y = int(floor(mLevelRender->mNewY)) >> 4;
	mBaseX = X - MAXHALFSIZE;
	mBaseZ = Z - MAXHALFSIZE;
	int dx = X-mOrgX;
	int dz = Z-mOrgZ;
	mOrgX = X;
	mOrgZ = Z;
	mOrgY = Y;

	nEnq = MAXUPDATE;

	if(!initialized)
	{
		loadSections();
		initialized = true;
	}
	else if(dx || dz)
	{
		//mLevel->logfile << dx <<" " << dz << endl;
		shiftEnqueueSections(dx,dz);
	} else {
		enqueueSections();
	}
	processUpdateQueue();	
}

void WorldRender::loadSections()
{
	for(int i=-mViewDistance;i<=mViewDistance;i++)
	{
		for(int j=-mViewDistance;j<=mViewDistance;j++)
		{
			int newZ = i+mOrgZ;
			int newX = j+mOrgX;
			
			for(int k=0;k!=MAXY;k++)
			{
				mSectionRenders[mSectionRendersIndex][i+MAXHALFSIZE][j+MAXHALFSIZE][k]->setPosition(newX,k,newZ);
				//mSectionRenders[i][j][k]->update();
			}
		}
	}
}

void WorldRender::render()
{
	//sort(mVisibleSectionRenders.begin(),mVisibleSectionRenders.end(),SectionRenderSorter(mOrgX,mOrgY,mOrgZ));
	glEnable(GL_TEXTURE_2D);
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);
	glEnable(GL_DEPTH_TEST);
	glDepthFunc(GL_LEQUAL);
	glEnable(GL_ALPHA_TEST);
	glAlphaFunc(GL_GREATER, 0.5);
	glBindTexture(GL_TEXTURE_2D,TextureManager::getInstance()->getTexture("terrain")->id);
	for(deque<SectionRender*>::iterator it = mVisibleSectionRenders.begin();
		it!=mVisibleSectionRenders.end();it++)
	{
		glPushMatrix();
		glTranslatef((*it)->mX*16,(*it)->mY*16,(*it)->mZ*16);
		(*it)->render();
		glPopMatrix();
		//break;
	}
	glBindTexture(GL_TEXTURE_2D,0);
}
 

void WorldRender::shiftEnqueueSections(int dx,int dz) 
{
	mVisibleSectionRenders.clear();
	int newIndex = (mSectionRendersIndex+1)%2;
	int i=0,j=0,di=0,dj=-1;
	int n = mFullDistance;
	int m = n;
	for(int t=0;t!= n*n ;t++)
	{
		if( -n/2<=i && i <=n/2 && -n/2<=j && j<=n/2)
		{

			int z = i+MAXHALFSIZE;
			int x = j+MAXHALFSIZE;

			int newZ = (i+dz+mViewDistance+mFullDistance)%mFullDistance+MAXHALFSIZE-mViewDistance;
			int newX = (j+dx+mViewDistance+mFullDistance)%mFullDistance+MAXHALFSIZE-mViewDistance;

			//printf("i: %d j: %d old: %d %d new: %d %d dt: %d %d\n",i,j,z,x,newZ,newX,dz,dx);
			for(int k=0;k!=MAXY;k++)
			{
				mSectionRenders[newIndex][z][x][k] = mSectionRenders[mSectionRendersIndex][newZ][newX][k];
				mSectionRenders[newIndex][z][x][k]->setPosition(mOrgX+j,k,mOrgZ+i);

				if(mLevelRender->mFrustum->AABBInFrustum(mSectionRenders[newIndex][z][x][k]->getAABB()))
				{
					if( abs(mOrgY-k)<=mViewDistance )
					{						
						mVisibleSectionRenders.push_back(mSectionRenders[newIndex][z][x][k]);

						if(mSectionRenders[newIndex][z][x][k]->mSection&&
							mSectionRenders[newIndex][z][x][k]->mSection->isDirty)
							mSectionRenders[newIndex][z][x][k]->isDirty=true;						
						if(mSectionRenders[newIndex][z][x][k]->isDirty && !mSectionRenders[newIndex][z][x][k]->inQueue)
						if(nEnq>=0 && nEnq--)
						{
							mSectionRenders[newIndex][z][x][k]->inQueue = true;
							mUpdateQueue.push_back(mSectionRenders[newIndex][z][x][k]);
						}
					}
				}
			}
		}
		if((i==j)|| (i<0 && i==-j) || (i>0 && i==1-j))
		{
			m = di;
			di = -dj;
			dj = m;
		}
		i+=di;
		j+=dj;
	}
	mSectionRendersIndex = newIndex;
}

void WorldRender::enqueueSections()
{
	mVisibleSectionRenders.clear();
	int i=0,j=0,di=0,dj=-1;
	int n = mFullDistance;
	int m = n;
	for(int t=0;t!= n*n ;t++)
	{
		if( -n/2<=i && i <=n/2 && -n/2<=j && j<=n/2)
		{
			int z = i+MAXHALFSIZE;
			int x = j+MAXHALFSIZE;

			for(int k=0;k!=MAXY;k++)
			{
				if(mLevelRender->mFrustum->AABBInFrustum(mSectionRenders[mSectionRendersIndex][z][x][k]->getAABB()))
				{
					if(abs(mOrgY-k)<=mViewDistance+1 )
					{						
						mVisibleSectionRenders.push_back(mSectionRenders[mSectionRendersIndex][z][x][k]);
						
						if(mSectionRenders[mSectionRendersIndex][z][x][k]->mSection && 
							mSectionRenders[mSectionRendersIndex][z][x][k]->mSection->isDirty)
							mSectionRenders[mSectionRendersIndex][z][x][k]->isDirty = true;
						if(mSectionRenders[mSectionRendersIndex][z][x][k]->isDirty && !mSectionRenders[mSectionRendersIndex][z][x][k]->inQueue)
						if(nEnq>=0 && nEnq--)
						{

							mSectionRenders[mSectionRendersIndex][z][x][k]->inQueue = true;
							mUpdateQueue.push_back(mSectionRenders[mSectionRendersIndex][z][x][k]);
						}
					}
				}
			}
		}
		if((i==j)|| (i<0 && i==-j) || (i>0 && i==1-j))
		{
			m = di;
			di = -dj;
			dj = m;
		}
		i+=di;
		j+=dj;
	}
}

void WorldRender::processUpdateQueue()
{
	if(mUpdateQueue.empty()) return;
	//if(frame%10==0)
	//{
	insertion_sort(mUpdateQueue.begin(),mUpdateQueue.end(),SectionRenderSorter(mOrgX,mOrgY,mOrgZ));
	//cout << mUpdateQueue.size() << endl;
	//	if(frame > 10000000)
	//		frame = 0;
	//}

	int cap = MAXUPDATE;
	if(cap > mUpdateQueue.size()) cap = mUpdateQueue.size();
	for(int i=0;i!=cap;i++)
	{
		mUpdateQueue.front()->update();
		mUpdateQueue.front()->inQueue = false;
   		mUpdateQueue.pop_front();
	}
}


const int WorldRender::MAXSIZE = 33;
const int WorldRender::MAXHALFSIZE = 16;
const int WorldRender::MINSIZE = 5;
const int WorldRender::MINHALFSIZE = 2;
const int WorldRender::MAXY = 16;
const int WorldRender::MAXUPDATE = 3;



WorldRender::SectionRenderSorter::SectionRenderSorter(int _x,int _y,int _z):
x(_x),
y(_y),
z(_z)
{

}
int WorldRender::SectionRenderSorter::squareDistance(SectionRender* it)
{
	return (it->mX-x)*(it->mX-x)+(it->mY-y)*(it->mY-y)+(it->mZ-z)*(it->mZ-z);
}

bool WorldRender::SectionRenderSorter::operator()(SectionRender* a,SectionRender* b)
{
	return squareDistance(a)<squareDistance(b);
}
