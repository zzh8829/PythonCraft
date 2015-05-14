#include "Texture.h"

Texture::Texture():
id(0),
minU(0),
maxU(0),
minV(0),
maxV(0),
width(0),
height(0),
size(0)
{
}

double Texture::getMinU()
{
	return minU;
}
double Texture::getMinV()
{
	return minV;
}
double Texture::getMaxU()
{
	return maxU;
}
double Texture::getMaxV()
{
	return maxV;
}
double Texture::getInterpolatedU(double d)
{
    return minU + (maxU - minU)*(d/16.0F);
}
double Texture::getInterpolatedV(double d)
{
	return (minV + (maxV - minV)*(d/16.0F));
}