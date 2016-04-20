#ifndef _NIBBLEARRAY_H_
#define _NIBBLEARRAY_H_

#include "CommonInc.h"

class NibbleArray
{
public:
	NibbleArray(int size);
	virtual ~NibbleArray();

	uint8_t getAt(int,int,int);
	void setAt(int,int,int,uint8_t data);
	void setData(std::vector<uint8_t>);

//private:
	uint8_t* mData;
};

#endif