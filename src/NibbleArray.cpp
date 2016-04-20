#include "NibbleArray.h"
using namespace std;
NibbleArray::NibbleArray(int size)
{
	mData = new uint8_t[size/2];
}

NibbleArray::~NibbleArray()
{
	delete[] mData;
}

uint8_t NibbleArray::getAt(int x,int y,int z)
{
	int idx = y << 8 | z << 4 | x;
	//return ((idx&1)? mData[idx>>1] >> 4 : mData[idx>>1])&15;
	return (uint8_t)(mData[idx / 2] >> ((idx) % 2 * 4) & 0xF);
}

void NibbleArray::setAt(int x,int y,int z,uint8_t data)
{
	int idx = y << 8 | z << 4 | x;
	data&=0xf;
	mData[idx/2] &= (uint8_t)(0xF << ((idx + 1) % 2 * 4));
    mData[idx/2] |= (uint8_t)(data << (idx % 2 * 4));
}

void NibbleArray::setData(vector<uint8_t> data)
{
	copy(data.begin(),data.end(),mData);
}