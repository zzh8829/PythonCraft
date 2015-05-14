#include "BlockRender.h"
#include "Texture.h"
#include "TextureManager.h"
using namespace std;
BlockRender::BlockRender(Level* level, int x,int y,int z):
mLevel(level)
{
	mSection = mLevel->getWorld()->getChunkData(x,z)->getSection(y);
	for(int i=0;i!=6;i++)
	{
		int tx = x + DELTAFACE[i][0];
		int ty = y + DELTAFACE[i][1];
		int tz = z + DELTAFACE[i][2];
		if(ty>=0 && ty<16)
			mAdjSections[i] = mLevel->getWorld()->getChunkData(tx,tz)->getSection(ty);
		else
			mAdjSections[i]=0;
	}
	mBuilder = QuadBuilder::getInstance();
}


void BlockRender::renderTopFace(Block* block,int x,int y,int z,int r,int g,int b)
{
	if(block->id == 2)
	{
		int color = -7226023;
		r = color >> 16 & 255;
		g = color >> 8 & 255;
		b = color & 255;
	}

	Texture* tex = TextureManager::getInstance()->getTexture(block->getTexName(0,mSection->getMetaData(x,y,z)));
	//cout << tex->id << endl;
	if(!tex)
	{
		cout << block->getTexName(0,mSection->getMetaData(x,y,z)) << endl;
		return;
	}
	
	mBuilder->setColori(r,g,b);

	mBuilder->setTexCoord(tex->minU, tex->maxV);
	mBuilder->addVertex(x,y+1,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->maxV);
	mBuilder->addVertex(x+1,y+1,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->minV);
	mBuilder->addVertex(x+1,y+1,z);
	mBuilder->setTexCoord(tex->minU, tex->minV);
	mBuilder->addVertex(x,y+1,z);
}

void BlockRender::renderBotFace(Block* block,int x,int y,int z,int r,int g,int b)
{
	Texture* tex = TextureManager::getInstance()->getTexture(block->getTexName(1,mSection->getMetaData(x,y,z)));
	//cout << tex->id << endl;
	if(!tex)
	{
		cout << block->getTexName(1,mSection->getMetaData(x,y,z)) << endl;
		return;
	}
	
	mBuilder->setColori(r*0.5,r*0.5,r*0.5);
	mBuilder->setTexCoord(tex->minU, tex->maxV);
	mBuilder->addVertex(x,y,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->maxV);
	mBuilder->addVertex(x+1,y,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->minV);	
	mBuilder->addVertex(x+1,y,z);
	mBuilder->setTexCoord(tex->minU, tex->minV);
	mBuilder->addVertex(x,y,z);

}

void BlockRender::renderZPosFace(Block* block,int x,int y,int z,int r,int g,int b)
{
	Texture* tex = TextureManager::getInstance()->getTexture(block->getTexName(2,mSection->getMetaData(x,y,z)));
	//cout << tex->id << endl;
	if(!tex)
	{
		cout << block->getTexName(2,mSection->getMetaData(x,y,z)) << endl;
		return;
	}
	
	mBuilder->setColori(r*0.8,g*0.8,b*0.8);
	mBuilder->setTexCoord(tex->minU, tex->maxV);
	mBuilder->addVertex(x,y,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->maxV);
	mBuilder->addVertex(x+1,y,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->minV);
	mBuilder->addVertex(1+x,y+1,z+1);
	mBuilder->setTexCoord(tex->minU, tex->minV);
	mBuilder->addVertex(x,y+1,z+1);
}

void BlockRender::renderXPosFace(Block* block,int x,int y,int z,int r,int g,int b)
{
	Texture* tex = TextureManager::getInstance()->getTexture(block->getTexName(3,mSection->getMetaData(x,y,z)));
	//cout << tex->id << endl;
	if(!tex)
	{
		cout << block->getTexName(3,mSection->getMetaData(x,y,z)) << endl;
		return;
	}
	
	mBuilder->setColori(r*0.6,g*0.6,b*0.6);

	mBuilder->setTexCoord(tex->minU, tex->maxV);
	mBuilder->addVertex(x+1,y,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->maxV);
	mBuilder->addVertex(x+1,y,z);
	mBuilder->setTexCoord(tex->maxU, tex->minV);
	mBuilder->addVertex(x+1,y+1,z);
	mBuilder->setTexCoord(tex->minU, tex->minV);
	mBuilder->addVertex(x+1,y+1,z+1);
}

void BlockRender::renderZNegFace(Block* block,int x,int y,int z,int r,int g,int b)
{
	Texture* tex = TextureManager::getInstance()->getTexture(block->getTexName(4,mSection->getMetaData(x,y,z)));
	//cout << tex->id << endl;
	if(!tex)
	{
		cout << block->getTexName(4,mSection->getMetaData(x,y,z))<< endl;
		return;
	}
	
	mBuilder->setColori(r*0.8,g*0.8,b*0.8);

	mBuilder->setTexCoord(tex->minU, tex->maxV);
	mBuilder->addVertex(x+1,y,z);
	mBuilder->setTexCoord(tex->maxU, tex->maxV);
	mBuilder->addVertex(x,y,z);
	mBuilder->setTexCoord(tex->maxU, tex->minV);
	mBuilder->addVertex(x,y+1,z);
	mBuilder->setTexCoord(tex->minU, tex->minV);
	mBuilder->addVertex(x+1,y+1,z);
}

void BlockRender::renderXNegFace(Block* block,int x,int y,int z,int r,int g,int b)
{	
	Texture* tex = TextureManager::getInstance()->getTexture(block->getTexName(5,mSection->getMetaData(x,y,z)));
	//cout << tex->id << endl;
	if(!tex)
	{
		cout << block->getTexName(5,mSection->getMetaData(x,y,z)) << endl;
		return;
	}
	
	mBuilder->setColori(r*0.6,g*0.6,b*0.6);

	mBuilder->setTexCoord(tex->minU, tex->maxV);
	mBuilder->addVertex(x,y,z);
	mBuilder->setTexCoord(tex->maxU, tex->maxV);
	mBuilder->addVertex(x,y,z+1);
	mBuilder->setTexCoord(tex->maxU, tex->minV);
	mBuilder->addVertex(x,y+1,z+1);
	mBuilder->setTexCoord(tex->minU, tex->minV);
	mBuilder->addVertex(x,y+1,z);	

}

void BlockRender::renderBlockNormal(Block* block,int x,int y,int z)
{
	int r = 255;
	int g = 255;
	int b = 255;
	if(block->id == 18)
	{
		int color = 6396257;
		r = color >> 16 & 255;
		g = color >> 8 & 255;
		b = color & 255;
	}
	if( shouldRender(block,x,y,z,0 ))renderTopFace(block,x,y,z,r,g,b);
	if( shouldRender(block,x,y,z,1 ))renderBotFace(block,x,y,z,r,g,b);
	if( shouldRender(block,x,y,z,2 ))renderZPosFace(block,x,y,z,r,g,b);
	if( shouldRender(block,x,y,z,3 ))renderXPosFace(block,x,y,z,r,g,b);
	if( shouldRender(block,x,y,z,4 ))renderZNegFace(block,x,y,z,r,g,b);
	if( shouldRender(block,x,y,z,5 ))renderXNegFace(block,x,y,z,r,g,b);
}

void BlockRender::renderBlockWater(Block* block,int x,int y,int z)
{
	if( getAdjId(block,x,y,z,0 )==0)renderTopFace(block,x,y,z,255,255,255);
	//if( getAdjId(block,x,y,z,1)==0 ) renderBotFace(block,x,y,z,255,255,255);
	//if( getAdjId(block,x,y,z,2)==0 ) renderZNegFace(block,x,y,z,255,255,255);
	//if( getAdjId(block,x,y,z,3)==0 ) renderXPosFace(block,x,y,z,255,255,255);
	//if( getAdjId(block,x,y,z,4)==0 ) renderZPosFace(block,x,y,z,255,255,255);
	//if( getAdjId(block,x,y,z,5)==0 ) renderXNegFace(block,x,y,z,255,255,255);
}

void BlockRender::renderBlockFlower(Block* block,int x,int y,int z)
{

	int color = block->getColor(mSection, x, y, z);

	int r = color >> 16 & 255;
	int g = color >> 8 & 255;
	int b = color & 255;

	mBuilder->setColori(r,g,b);

	double xx = (double)x;
	double yy = (double)y;
	double zz = (double)z;

	if (block->id == 31)
	{
	    int64_t tmp = (int64_t)(x * 3129871) ^ (int64_t)z * 116129781ll ^ (int64_t)y;
	    tmp = tmp * tmp * 42317861ll + tmp * 11ll;
	    xx += ((double)((float)(tmp >> 16 & 15ll) / 15.0F) - 0.5) * 0.5;
	    yy += ((double)((float)(tmp >> 20 & 15ll) / 15.0F) - 1.0) * 0.2;
	    zz += ((double)((float)(tmp >> 24 & 15ll) / 15.0F) - 0.5) * 0.5;
	}

	//this.drawCrossedSquares(par1Block, this.blockAccess.getBlockMetadata(x, y, z), var19, var20, var15, 1.0F);

	Texture* tex = TextureManager::getInstance()->getTexture(
		block->getTexName(0,mSection->getMetaData(x,y,z)));

	double var20 = 0.45 * (double)1;
	double var22 = xx + 0.5 - var20;
	double var24 = xx + 0.5 + var20;
	double var26 = zz + 0.5 - var20;
	double var28 = zz + 0.5 + var20;

	mBuilder->addVertexWithUV(var22, yy + 1, var26, tex->minU, tex->minV);
	mBuilder->addVertexWithUV(var22, yy + 0, var26, tex->minU, tex->maxV);
	mBuilder->addVertexWithUV(var24, yy + 0, var28, tex->maxU, tex->maxV);
	mBuilder->addVertexWithUV(var24, yy + 1, var28, tex->maxU, tex->minV);

	/*
	mBuilder->addVertexWithUV(var24, yy + 1, var28, tex->minU, tex->minV);
	mBuilder->addVertexWithUV(var24, yy + 0, var28, tex->minU, tex->maxV);
	mBuilder->addVertexWithUV(var22, yy + 0, var26, tex->maxU, tex->maxV);
	mBuilder->addVertexWithUV(var22, yy + 1, var26, tex->maxU, tex->minV);
	*/
	
	mBuilder->addVertexWithUV(var22, yy + 1, var28, tex->minU, tex->minV);
	mBuilder->addVertexWithUV(var22, yy + 0, var28, tex->minU, tex->maxV);
	mBuilder->addVertexWithUV(var24, yy + 0, var26, tex->maxU, tex->maxV);
	mBuilder->addVertexWithUV(var24, yy + 1, var26, tex->maxU, tex->minV);

	/*
	mBuilder->addVertexWithUV(var24, yy + 1, var26, tex->minU, tex->minV);
	mBuilder->addVertexWithUV(var24, yy + 0, var26, tex->minU, tex->maxV);
	mBuilder->addVertexWithUV(var22, yy + 0, var28, tex->maxU, tex->maxV);
	mBuilder->addVertexWithUV(var22, yy + 1, var28, tex->maxU, tex->minV);
	*/
	
}

void BlockRender::renderBlockTorchAtAngle(Block* block, double par2, double par4, double par6, double par8, double par10, int par12)
{	
	QuadBuilder* builder = QuadBuilder::getInstance();
	Texture * tex = TextureManager::getInstance()->getTexture(block->getTexName(0,par12));

	double var15 = tex->getMinU();
	double var17 = tex->getMinV();
	double var19 = tex->getMaxU();
	double var21 = tex->getMaxV();
	double var23 = tex->getInterpolatedU(7.0);
	double var25 = tex->getInterpolatedV(6.0);
	double var27 = tex->getInterpolatedU(9.0);
	double var29 = tex->getInterpolatedV(8.0);
	double var31 = tex->getInterpolatedU(7.0);
	double var33 = tex->getInterpolatedV(13.0);
	double var35 = tex->getInterpolatedU(9.0);
	double var37 = tex->getInterpolatedV(15.0);
	par2 += 0.5;
	par6 += 0.5;
	double var39 = par2 - 0.5;
	double var41 = par2 + 0.5;
	double var43 = par6 - 0.5;
	double var45 = par6 + 0.5;
	double var47 = 0.0625;
	double var49 = 0.625;
	builder->addVertexWithUV(par2 + par8 * (1.0 - var49) - var47, par4 + var49, par6 + par10 * (1.0 - var49) - var47, var23, var25);
	builder->addVertexWithUV(par2 + par8 * (1.0 - var49) - var47, par4 + var49, par6 + par10 * (1.0 - var49) + var47, var23, var29);
	builder->addVertexWithUV(par2 + par8 * (1.0 - var49) + var47, par4 + var49, par6 + par10 * (1.0 - var49) + var47, var27, var29);
	builder->addVertexWithUV(par2 + par8 * (1.0 - var49) + var47, par4 + var49, par6 + par10 * (1.0 - var49) - var47, var27, var25);
	builder->addVertexWithUV(par2 + var47 + par8, par4, par6 - var47 + par10, var35, var33);
	builder->addVertexWithUV(par2 + var47 + par8, par4, par6 + var47 + par10, var35, var37);
	builder->addVertexWithUV(par2 - var47 + par8, par4, par6 + var47 + par10, var31, var37);
	builder->addVertexWithUV(par2 - var47 + par8, par4, par6 - var47 + par10, var31, var33);
	builder->addVertexWithUV(par2 - var47, par4 + 1.0, var43, var15, var17);
	builder->addVertexWithUV(par2 - var47 + par8, par4 + 0.0, var43 + par10, var15, var21);
	builder->addVertexWithUV(par2 - var47 + par8, par4 + 0.0, var45 + par10, var19, var21);
	builder->addVertexWithUV(par2 - var47, par4 + 1.0, var45, var19, var17);
	builder->addVertexWithUV(par2 + var47, par4 + 1.0, var45, var15, var17);
	builder->addVertexWithUV(par2 + par8 + var47, par4 + 0.0, var45 + par10, var15, var21);
	builder->addVertexWithUV(par2 + par8 + var47, par4 + 0.0, var43 + par10, var19, var21);
	builder->addVertexWithUV(par2 + var47, par4 + 1.0, var43, var19, var17);
	builder->addVertexWithUV(var39, par4 + 1.0, par6 + var47, var15, var17);
	builder->addVertexWithUV(var39 + par8, par4 + 0.0, par6 + var47 + par10, var15, var21);
	builder->addVertexWithUV(var41 + par8, par4 + 0.0, par6 + var47 + par10, var19, var21);
	builder->addVertexWithUV(var41, par4 + 1.0, par6 + var47, var19, var17);
	builder->addVertexWithUV(var41, par4 + 1.0, par6 - var47, var15, var17);
	builder->addVertexWithUV(var41 + par8, par4 + 0.0, par6 - var47 + par10, var15, var21);
	builder->addVertexWithUV(var39 + par8, par4 + 0.0, par6 - var47 + par10, var19, var21);
	builder->addVertexWithUV(var39, par4 + 1.0, par6 - var47, var19, var17);
}

void BlockRender::renderBlockTorch(Block* block,int x,int y,int z)
{
	int meta = mSection->getMetaData(x,y,z);

    mBuilder->setColori(255,255,255);

    double t1 = 0.4000000059604645;
    double t2 = 0.5 - t1;
    double t3 = 0.20000000298023224;

    if (meta == 1)
    {
        renderBlockTorchAtAngle(block, x - t2, y + t3, z, -t1, 0.0, meta);
    }
    else if (meta == 2)
    {
        renderBlockTorchAtAngle(block, x + t2, y + t3, z, t1, 0.0, meta);
    }
    else if (meta == 3)
    {
        renderBlockTorchAtAngle(block, x, y + t3, z - t2, 0.0, -t1, meta);
    }
    else if (meta == 4)
    {
        renderBlockTorchAtAngle(block, x, y + t3, z + t2, 0.0, t1, meta);
    }
    else
    {
        renderBlockTorchAtAngle(block, x, y, z, 0.0, 0.0, meta);
    }	
}

void BlockRender::renderBlockStairs(Block* block,int x,int y,int z)
{
	int meta = mSection->getMetaData(x,y,z);
	Texture* tex = TextureManager::getInstance()->getTexture(block->getTexName(0,meta));

	int r = 255,g=255,b=255;
	mBuilder->setColori(r,g,b);

	//top
	mBuilder->addVertexWithUV(x,y+0.5,z+1,tex->getMinU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x+0.5,y+0.5,z+1,tex->getInterpolatedU(8),tex->getMaxV());
	mBuilder->addVertexWithUV(x+0.5,y+0.5,z,tex->getInterpolatedU(8),tex->getMinV());
	mBuilder->addVertexWithUV(x,y+0.5,z,tex->getMinU(),tex->getMinV());

	mBuilder->addVertexWithUV(x+0.5,y+1,z+1,tex->getInterpolatedU(8),tex->getMaxV());
	mBuilder->addVertexWithUV(x+1,y+1,z+1,tex->getMaxU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x+1,y+1,z,tex->getMaxU(),tex->getMinV());
	mBuilder->addVertexWithUV(x+0.5,y+1,z,tex->getInterpolatedU(8),tex->getMinV());

	//bot
	renderBotFace(block,x,y,z,255,255,255);

	tex = TextureManager::getInstance()->getTexture(block->getTexName(2,meta));

	mBuilder->setColori(r*0.8,r*0.8,r*0.8);
	//front
	mBuilder->addVertexWithUV(x,y,z+1,tex->getMinU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x+0.5,y,z+1,tex->getInterpolatedU(8),tex->getMaxV());
	mBuilder->addVertexWithUV(x+0.5,y+0.5,z+1,tex->getInterpolatedU(8),tex->getInterpolatedV(8));
	mBuilder->addVertexWithUV(x,y+0.5,z+1,tex->getMinU(),tex->getInterpolatedV(8));

	mBuilder->addVertexWithUV(x+0.5,y,z+1,tex->getInterpolatedU(8),tex->getMaxV());
	mBuilder->addVertexWithUV(x+1,y,z+1,tex->getMaxU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x+1,y+1,z+1,tex->getMaxU(),tex->getMinV());
	mBuilder->addVertexWithUV(x+0.5,y+1,z+1,tex->getInterpolatedU(8),tex->getMinV());

	tex = TextureManager::getInstance()->getTexture(block->getTexName(4,meta));

	//back
	mBuilder->addVertexWithUV(x+1,y,z,tex->getMinU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x+0.5,y,z,tex->getInterpolatedU(8),tex->getMaxV());
	mBuilder->addVertexWithUV(x+0.5,y+1,z,tex->getInterpolatedU(8),tex->getMinV());
	mBuilder->addVertexWithUV(x+1,y+1,z,tex->getMinU(),tex->getMinV());

	mBuilder->addVertexWithUV(x+0.5,y,z,tex->getInterpolatedU(8),tex->getMaxV());
	mBuilder->addVertexWithUV(x,y,z,tex->getMaxU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x,y+0.5,z,tex->getMaxU(),tex->getInterpolatedV(8));
	mBuilder->addVertexWithUV(x+0.5,y+0.5,z,tex->getInterpolatedU(8),tex->getInterpolatedV(8));

	tex = TextureManager::getInstance()->getTexture(block->getTexName(5,meta));

	mBuilder->setColori(r*0.6,r*0.6,r*0.6);
	//left
	mBuilder->addVertexWithUV(x,y,z,tex->getMinU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x,y,z+1,tex->getMaxU(),tex->getMaxV());
	mBuilder->addVertexWithUV(x,y+0.5,z+1,tex->getMaxU(),tex->getInterpolatedV(8));
	mBuilder->addVertexWithUV(x,y+0.5,z,tex->getMinU(),tex->getInterpolatedV(8));

	mBuilder->addVertexWithUV(x+0.5,y+0.5,z,tex->getMinU(),tex->getInterpolatedV(8));
	mBuilder->addVertexWithUV(x+0.5,y+0.5,z+1,tex->getMaxU(),tex->getInterpolatedV(8));
	mBuilder->addVertexWithUV(x+0.5,y+1,z+1,tex->getMaxU(),tex->getMinV());
	mBuilder->addVertexWithUV(x+0.5,y+1,z,tex->getMinU(),tex->getMinV());

	//right
	renderXPosFace(block,x,y,z,255,255,255);
}

bool BlockRender::renderBlock(int id,int x, int y,int z)
{
	Block* block = Block::BlockList[id];
	if(block)
	{
		if(block->id)
		{
			switch(block->renderType)
			{
			case Block::RenderType::NORMAL:
				renderBlockNormal(block,x,y,z);
				break;
			case Block::RenderType::FLOWER:
				renderBlockFlower(block,x,y,z);
				break;
			case Block::RenderType::TORCH:
				renderBlockTorch(block,x,y,z);
				break;
			case Block::RenderType::STAIRS:
				renderBlockStairs(block,x,y,z);
				break;
			case Block::RenderType::LILYPAD:
				if(shouldRender(block,x,y,z,1 ))renderBotFace(block,x,y,z,255,255,255);
				break;
			case Block::RenderType::DOOR:
				break;
			case Block::RenderType::NO:
				break;
			default:
				renderBlockNormal(block,x,y,z);

			}
		}
		return true;
	}
	return false;
}

bool BlockRender::shouldRender(Block* block,int x,int y,int z,int face)
{
	int tx = x+DELTAFACE[face][0];
	int ty = y+DELTAFACE[face][1];
	int tz = z+DELTAFACE[face][2];
	Section* section = mSection;
	if(tx<0 || tx >=16 || ty< 0 || ty>=16 || tz<0 || tz >=16)
	{
		section = mAdjSections[face];
		if(!section) return 1;
	}
	int id = section->getBlockId(tx&15,ty&15,tz&15);
	return !id || (Block::BlockList[id]->transparent == 1 && id!=block->id);
}

int BlockRender::getAdjId(Block* block,int x,int y,int z,int face)
{
	int tx = x+DELTAFACE[face][0];
	int ty = y+DELTAFACE[face][1];
	int tz = z+DELTAFACE[face][2];
	Section* section = mSection;
	if(tx<0 || tx >=16 || ty< 0 || ty>=16 || tz<0 || tz >=16)
	{
		section = mAdjSections[face];
		if(!section) return 0;
	}
	return section->getBlockId(tx&15,ty&15,tz&15);
}


const int BlockRender::DELTAFACE[6][3] = {
	{0,1,0},
	{0,-1,0},
	{0,0,1},
	{1,0,0},
	{0,0,-1},
	{-1,0,0}
};
