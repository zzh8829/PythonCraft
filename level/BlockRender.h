#ifndef _BLOCKSRENDER_H_
#define _BLOCKSRENDER_H_

#include "CommonInc.h"
#include "Level.h"
#include "Block.h"
#include "Section.h"
#include "QuadBuilder.h"

class BlockRender
{
public:
	BlockRender(Level*,int,int,int);

	void renderTopFace(Block*,int,int,int,int,int,int);
	void renderBotFace(Block*,int,int,int,int,int,int);
	void renderZNegFace(Block*,int,int,int,int,int,int);
	void renderXPosFace(Block*,int,int,int,int,int,int);
	void renderZPosFace(Block*,int,int,int,int,int,int);
	void renderXNegFace(Block*,int,int,int,int,int,int);

	bool renderBlock(int,int,int,int);
	void renderBlockNormal(Block*,int,int,int);
	void renderBlockFlower(Block*,int,int,int);
	void renderBlockTorch(Block*,int,int,int);
	void renderBlockTorchAtAngle(Block*,double,double,double,double,double,int);
	void renderBlockWater(Block* block,int x,int y,int z);
	void renderBlockStairs(Block* block,int x,int y,int z);
	void renderBlockHalf(Block* block,int x,int y,int z);

	
	int getAdjId(Block* block,int x,int y,int z,int face);

	bool shouldRender(Block* block,int,int,int,int);
	//bool renderTextureMissingBlock(int,int,int,int);


	Level* mLevel;
	Section* mSection;
	Section* mAdjSections[6];
	QuadBuilder* mBuilder;
	static const int DELTAFACE[6][3];
};

#endif