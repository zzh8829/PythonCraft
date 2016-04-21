#include "SectionRender.h"
#include "TextureManager.h"
#include "Block.h"
#include "BlockRender.h"
using namespace std;

const int SectionRender::DELTAFACE[6][3] = {
	{0,1,0},
	{0,-1,0},
	{0,0,-1},
	{1,0,0},
	{0,0,1},
	{-1,0,0}
};

void SectionRender::update()
{
	if(isDirty)
	{
		mSection = mLevel->getWorld()->getChunkData(mX,mZ)->getSection(mY);
		for(int i=0;i!=6;i++)
		{
			int tx = mX + DELTAFACE[i][0];
			int ty = mY + DELTAFACE[i][1];
			int tz = mZ + DELTAFACE[i][2];
			if(ty>=0 && ty<16)
				mAdjSections[i] = mLevel->getWorld()->getChunkData(tx,tz)->getSection(ty);
		}


		//if(mY != 5) return;
		//mLevel->logfile << "Updating Section " << mX<< " " << mY<< " " << mZ << std::endl;
		//mLevel->logfile.flush();
		//printf("Updating Section: %d %d %d\n",mX,mY,mZ);
		if(mDisplayList) glDeleteLists(mDisplayList,1);
		mDisplayList = glGenLists(1);
		glNewList(mDisplayList,GL_COMPILE);
		glPushMatrix();

		glColor3f(1,1,1);

		QuadBuilder* builder = QuadBuilder::getInstance();
		builder->begin();

		BlockRender br(mLevel,mX,mY,mZ);


		for(int x=0;x!=16;x++)
		{
			for(int y=0;y!=16;y++)
			{
				for(int z=0;z!=16;z++)
				{
					uint8_t id = mSection->getBlockId(x,y,z);

					if(id)
					{
						if(!br.renderBlock(id,x,y,z))
						{
							//builder->setColori(rand()&255,rand()&255,rand()&255);
							int r = 123;
							int g = 123;
							int b = 123;
							//builder->setColori(123,123,123);
							// Top
							if( shouldRender(x,y,z,0 ))
							{
								builder->setColori(r,g,b);
								//builder->setNormal(0,1,0);

								//builder->setTexCoord(uvs[0][0][0],uvs[0][0][1])
								//builder->setColori(*colors[0])
								builder->addVertex(x,1+y,z);
								//builder->setTexCoord(uvs[0][1][0],uvs[0][1][1])
								////builder->setColori(*colors[0])
								builder->addVertex(1+x,1+y,z);
								//builder->setTexCoord(uvs[0][2][0],uvs[0][2][1])
								////builder->setColori(*colors[0])
								builder->addVertex(1+x,1+y,1+z);
								//builder->setTexCoord(uvs[0][3][0],uvs[0][3][1])
								////builder->setColori(*colors[0])
								builder->addVertex(x,1+y,1+z);
							}							
							// Bot
							if( shouldRender(x,y,z,1 ))
							{
								builder->setColori(r,g,b);
								//builder->setNormal(0,-1,0);

								//builder->setTexCoord(uvs[1][0][0],uvs[1][0][1])
								//builder->setColori(*colors[1])
								builder->addVertex(x,y,1+z);
								//builder->setTexCoord(uvs[1][1][0],uvs[1][1][1])
								////builder->setColori(*colors[1])
								builder->addVertex(1+x,y,1+z);
								//builder->setTexCoord(uvs[1][2][0],uvs[1][2][1])
								////builder->setColori(*colors[1])
								builder->addVertex(1+x,y,z);
								//builder->setTexCoord(uvs[1][3][0],uvs[1][3][1])
								////builder->setColori(*colors[1])
								builder->addVertex(x,y,z);

							}

							// Z Minus
							if( shouldRender(x,y,z,2 ))
							{
								builder->setColori(r*0.9,g*0.9,b*0.9);
								//builder->setNormal(0,0,-1);
								//builder->setTexCoord(uvs[2][0][0],uvs[2][0][1])
								//builder->setColori(*colors[2])
								builder->addVertex(x,y,z);
								//builder->setTexCoord(uvs[2][1][0],uvs[2][1][1])
								////builder->setColori(*colors[2])
								builder->addVertex(1+x,y,z);
								//builder->setTexCoord(uvs[2][2][0],uvs[2][2][1])
								////builder->setColori(*colors[2])
								builder->addVertex(1+x,1+y,z);
								//builder->setTexCoord(uvs[2][3][0],uvs[2][3][1])
								////builder->setColori(*colors[2])
								builder->addVertex(x,1+y,z);

							}

							// X Plus
							if( shouldRender(x,y,z,3 ))
							{
								builder->setColori(r*0.8,g*0.8,b*0.8);
								//builder->setNormal(1,0,0);
								//builder->setTexCoord(uvs[3][0][0],uvs[3][0][1])
								//builder->setColori(*colors[3])
								builder->addVertex(1+x,y,z);
								//builder->setTexCoord(uvs[3][1][0],uvs[3][1][1])
								////builder->setColori(*colors[3])
								builder->addVertex(1+x,y,1+z);
								//builder->setTexCoord(uvs[3][2][0],uvs[3][2][1])
								////builder->setColori(*colors[3])
								builder->addVertex(1+x,1+y,1+z);
								//builder->setTexCoord(uvs[3][3][0],uvs[3][3][1])
								////builder->setColori(*colors[3])
								builder->addVertex(1+x,1+y,z);

							}

							// Z Plus
							if( shouldRender(x,y,z,4 ))
							{
								builder->setColori(r*0.9,g*0.9,b*0.9);
								//builder->setNormal(0,0,1);
								//builder->setTexCoord(uvs[4][0][0],uvs[4][0][1])
								//builder->setColori(*colors[4])
								builder->addVertex(1+x,y,1+z);
								//builder->setTexCoord(uvs[4][1][0],uvs[4][1][1])
								////builder->setColori(*colors[4])
								builder->addVertex(x,y,1+z);
								//builder->setTexCoord(uvs[4][2][0],uvs[4][2][1])
								////builder->setColori(*colors[4])
								builder->addVertex(x,1+y,1+z);
								//builder->setTexCoord(uvs[4][3][0],uvs[4][3][1])
								////builder->setColori(*colors[4])
								builder->addVertex(1+x,1+y,1+z);

							}

							// X Minus
							if( shouldRender(x,y,z,5 ))
							{
								builder->setColori(r*0.8,g*0.8,b*0.8);
								//builder->setNormal(-1,0,0);
								//builder->setTexCoord(uvs[5][0][0],uvs[5][0][1])
								//builder->setColori(*colors[5])
								builder->addVertex(x,y,1+z);
								//builder->setTexCoord(uvs[5][1][0],uvs[5][1][1])
								////builder->setColori(*colors[5])
								builder->addVertex(x,y,z);
								//builder->setTexCoord(uvs[5][2][0],uvs[5][2][1])
								////builder->setColori(*colors[5])
								builder->addVertex(x,1+y,z);
								//builder->setTexCoord(uvs[5][3][0],uvs[5][3][1])
								////builder->setColori(*colors[5])
								builder->addVertex(x,1+y,1+z);

							}
						}
					}
				}
			}
		}
		builder->render();

		glPopMatrix();
		glEndList();

		isDirty = false;
		mSection->isDirty = false;
	}
}


void SectionRender::render()
{
	if(mDisplayList && !isDirty)
	{
		//mLevel->logfile << "Rendering Section " << mX<< " " << mY<< " " << mZ << std::endl;
		//mLevel->logfile.flush();
		//printf("Rendering Section: %d %d %d\n",mX,mY,mZ);
		//glBindTexture(GL_TEXTURE_2D,TextureManager::getInstance()->getTexture("terrain")->id);
		glCallList(mDisplayList);
	}
	
}

void SectionRender::setPosition(int x,int y,int z)
{
	if(mX!=x || mY!=y || mZ!=z || !mSection)
	{
		
		isDirty = true;

		mX = x;
		mY = y;
		mZ = z;
	}
}

bool SectionRender::shouldRender(int x,int y,int z,int face)
{
	int tx = x+DELTAFACE[face][0];
	int ty = y+DELTAFACE[face][1];
	int tz = z+DELTAFACE[face][2];
	if(0 <= tx && tx <16 && 0 <= ty && ty <16 && 0 <= tz && tz <16)
	{
		//printf("%d %d %d\n",tx,ty,tz);
		return !mSection->getBlockId(tx,ty,tz);
	} else 
	{
		if(mAdjSections[face])
			return !mAdjSections[face]->getBlockId(tx&15,ty&15,tz&15);
		return 1;
	}
}

AABB SectionRender::getAABB()
{
	return AABB(mX,mY,mZ,mX+16,mY+16,mZ+16);
}
