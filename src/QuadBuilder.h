#ifndef _QUADBUILDER_H_
#define _QUADBUILDER_H_

#include <SDL.h>
#include <SDL_opengl.h>

class QuadBuilder
{
public:
	QuadBuilder(int bufferSize)
	{
		maxVertex = bufferSize;
		mRawVertex = new double[maxVertex*3];
		mRawColor = new double[maxVertex*4];
		mRawNormal = new double[maxVertex*3];
		mRawTexCoord = new double[maxVertex*2];
		reset();
	}
	///*
	virtual ~QuadBuilder()
	{
		delete [] mRawVertex;
		delete [] mRawColor;
		delete [] mRawNormal;
		delete [] mRawTexCoord;
	}
	//*/
	static QuadBuilder* getInstance()
	{
		if(!mInstance)
			mInstance = new QuadBuilder(2000);
		return mInstance;
	}

	void begin()
	{
		begin(GL_QUADS,0);
	}

	void begin(int mode,int resetflag=0)
	{
		reset(resetflag);
		mMode = mode;
	}

	void render()
	{
		glEnableClientState(GL_VERTEX_ARRAY);
		glVertexPointer(3,GL_DOUBLE,0,mRawVertex);
		if(hasColor)
		{
			glEnableClientState(GL_COLOR_ARRAY);
			glColorPointer(4,GL_DOUBLE,0,mRawColor);
		}
		if(hasTexture)
		{
			glEnableClientState(GL_TEXTURE_COORD_ARRAY);
			glTexCoordPointer(2,GL_DOUBLE,0,mRawTexCoord);
		}
		if(hasNormal)
		{
			glEnableClientState(GL_NORMAL_ARRAY);
			glNormalPointer(GL_DOUBLE,0,mRawNormal);
		}

		glDrawArrays(mMode, 0, mNumVertex);

		glDisableClientState(GL_VERTEX_ARRAY);
		if(hasColor)
			glDisableClientState(GL_COLOR_ARRAY);
		if(hasTexture)
			glDisableClientState(GL_TEXTURE_COORD_ARRAY);
		if(hasNormal)
			glDisableClientState(GL_NORMAL_ARRAY);
	}

	void reset(int resetflag=0)
	{
		mNumVertex = 0;
		if(!resetflag)
		{
			hasColor = false;
			hasNormal = false;
			hasTexture = false;
		}
	}

	void setColor(double _r,double _g,double _b,double _a= 0)
	{
		hasColor = true;
		r = _r;
		g = _g;
		b = _b;
		a = _a;
	}

	void setColori(int _r,int _g,int _b,int _a = 255)
	{
		setColor(_r/255.0,_g/255.0,_b/255.0,_a/255.0);
	}

	void setNormal(double x,double y, double z)
	{
		hasNormal = true;
		nx = x;
		ny = y;
		nz = z;
	}

	void setTexCoord(double _u,double _v)
	{
		hasTexture = true;
		u = _u;
		v = _v;
	}

	void addVertexWithUV(double x,double y,double z,double u,double v)
	{
		setTexCoord(u,v);
		addVertex(x,y,z);
	}

	void addVertex(double x,double y, double z)
	{
		int v2 = mNumVertex<<1;
		int v3 = v2+mNumVertex;
		int v4 = v3+mNumVertex;

		mRawVertex[v3] = x;
		mRawVertex[v3+1] = y;
		mRawVertex[v3+2] = z;

		if(hasColor)
		{
			mRawColor[v4] = r;
			mRawColor[v4+1] = g;
			mRawColor[v4+2] = b;
			mRawColor[v4+3] = a;
		}
		if(hasNormal)
		{
			mRawNormal[v3] = nx;
			mRawNormal[v3+1] = ny;
			mRawNormal[v3+2] = nz;
		}
		if(hasTexture)
		{
			mRawTexCoord[v2] = u;
			mRawTexCoord[v2+1] = v;
		}
		mNumVertex++;

		if(mNumVertex+ 30 > maxVertex && mNumVertex % 12 ==0)
		{
			render();
			reset(1);
		}
	}
private:
	int maxVertex;
	int mNumVertex;
	int mMode;

	bool hasColor;
	bool hasNormal;
	bool hasTexture;

	double* mRawVertex;
	double* mRawColor;
	double* mRawNormal;
	double* mRawTexCoord;

	double r,g,b,a;
	double u,v;
	double nx,ny,nz;

	static QuadBuilder* mInstance;
};

#endif

