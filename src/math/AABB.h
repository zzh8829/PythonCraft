#ifndef _AABB_H_
#define _AABB_H_

class AABB
{
public:
	double minX;
	double minY;
	double minZ;
	double maxX;
	double maxY;
	double maxZ;
	AABB()
	{
		minX = 0;
		minY = 0;
		minZ = 0;
		maxX = 0;
		maxY = 0;
		maxZ = 0;
	}
	AABB(double minx, double miny, double minz, double maxx, double maxy, double maxz)
	{
		this->minX = minx;
		this->minY = miny;
		this->minZ = minz;
		this->maxX = maxx;
		this->maxY = maxy;
		this->maxZ = maxz;
	}

};

#endif