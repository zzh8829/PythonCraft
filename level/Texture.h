#ifndef _TEXTURE_H_
#define _TEXTURE_H_

#include "CommonInc.h"

class Texture
{
public:
	Texture();
	int id;
	double minU,minV,maxU,maxV;
	int width,height,size;

	double getMinU();
	double getMinV();
	double getMaxU();
	double getMaxV();
	double getInterpolatedU(double);
	double getInterpolatedV(double);
};

#endif