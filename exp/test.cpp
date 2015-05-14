#include <iostream>
#include <fstream>
#include <gl/gl.h>
#include <gl/glu.h>
using namespace std;

#include <boost/python.hpp>

using namespace boost::python;

class Vector3
{
public:
	float x,y,z;
	
	Vector3(float _x,float _y,float _z):x(_x),y(_y),z(_z){};

	Vector3 operator+ (const Vector3& other)
	{
		return Vector3(
			x + other.x,
			y + other.y,
			z + other.z
		);
	}

	Vector3 operator*(const Vector3& other)
	{ 
		return Vector3(
			y*other.z - z*other.y,
			z*other.x - x*other.z,
			x*other.y - y*other.x
		);
	}
	
};

ostream& operator<<(ostream& out,const Vector3& vec)
{
	out << vec.x << " " << vec.y << " " << vec.z;
}


class MeshBuilder
{
public:
	MeshBuilder(int bufferSize)
	{
		maxVertex = bufferSize;
		mRawVertex = new float[maxVertex*3];
		mRawColor = new float[maxVertex*4];
		mRawNormal = new float[maxVertex*3];
		mRawTexCoord = new float[maxVertex*2];
		reset();
	}
	///*
	virtual ~MeshBuilder()
	{
		delete [] mRawVertex;
		delete [] mRawColor;
		delete [] mRawNormal;
		delete [] mRawTexCoord;
	}
	//*/
	static const MeshBuilder& getInstance()
	{
		if(mInstance == NULL)
			mInstance = new MeshBuilder(2000);
		return *mInstance;
	}

	void begin(int mode)
	{
		reset();
		mMode = mode;
	}

	void render()
	{
		glEnableClientState(GL_VERTEX_ARRAY);
		glVertexPointer(3,GL_FLOAT,0,mRawVertex);
		if(hasColor)
		{
			glEnableClientState(GL_COLOR_ARRAY);
			glColorPointer(4,GL_FLOAT,0,mRawColor);
		}
		if(hasTexture)
		{
			glEnableClientState(GL_TEXTURE_COORD_ARRAY);
			glTexCoordPointer(2,GL_FLOAT,0,mRawTexCoord);
		}
		if(hasNormal)
		{
			glEnableClientState(GL_NORMAL_ARRAY);
			glNormalPointer(GL_FLOAT,0,mRawNormal);
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

	void reset()
	{
		mNumVertex = 0;
		hasColor = false;
		hasNormal = false;
		hasTexture = false;
	}

	void setColor(float _r,float _g,float _b,float _a= 0)
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

	void setNormal(float x,float y, float z)
	{
		hasNormal = true;
		nx = x;
		ny = y;
		nz = z;
	}

	void setTexCoord(float _u,float _v)
	{
		hasTexture = true;
		u = _u;
		v = _v;
	}

	void addVertex(float x,float y, float z)
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
			begin(mMode);
		}
	}
private:
	int maxVertex;
	int mNumVertex;
	int mMode;

	bool hasColor;
	bool hasNormal;
	bool hasTexture;

	float* mRawVertex;
	float* mRawColor;
	float* mRawNormal;
	float* mRawTexCoord;

	float r,g,b,a;
	float u,v;
	float nx,ny,nz;

	static MeshBuilder* mInstance;
};
MeshBuilder* MeshBuilder::mInstance = NULL;


void CUBE()
{
	glBegin(GL_QUADS);        // Draw The Cube Using quads
		glColor3f(0.0f,1.0f,0.0f);    // Color Blue
		glVertex3f( 1.0f, 1.0f,-1.0f);    // Top Right Of The Quad (Top)
		glVertex3f(-1.0f, 1.0f,-1.0f);    // Top Left Of The Quad (Top)
		glVertex3f(-1.0f, 1.0f, 1.0f);    // Bottom Left Of The Quad (Top)
		glVertex3f( 1.0f, 1.0f, 1.0f);    // Bottom Right Of The Quad (Top)
		glColor3f(1.0f,0.5f,0.0f);    // Color Orange
		glVertex3f( 1.0f,-1.0f, 1.0f);    // Top Right Of The Quad (Bottom)
		glVertex3f(-1.0f,-1.0f, 1.0f);    // Top Left Of The Quad (Bottom)
		glVertex3f(-1.0f,-1.0f,-1.0f);    // Bottom Left Of The Quad (Bottom)
		glVertex3f( 1.0f,-1.0f,-1.0f);    // Bottom Right Of The Quad (Bottom)
		glColor3f(1.0f,0.0f,0.0f);    // Color Red    
		glVertex3f( 1.0f, 1.0f, 1.0f);    // Top Right Of The Quad (Front)
		glVertex3f(-1.0f, 1.0f, 1.0f);    // Top Left Of The Quad (Front)
		glVertex3f(-1.0f,-1.0f, 1.0f);    // Bottom Left Of The Quad (Front)
		glVertex3f( 1.0f,-1.0f, 1.0f);    // Bottom Right Of The Quad (Front)
		glColor3f(1.0f,1.0f,0.0f);    // Color Yellow
		glVertex3f( 1.0f,-1.0f,-1.0f);    // Top Right Of The Quad (Back)
		glVertex3f(-1.0f,-1.0f,-1.0f);    // Top Left Of The Quad (Back)
		glVertex3f(-1.0f, 1.0f,-1.0f);    // Bottom Left Of The Quad (Back)
		glVertex3f( 1.0f, 1.0f,-1.0f);    // Bottom Right Of The Quad (Back)
		glColor3f(0.0f,0.0f,1.0f);    // Color Blue
		glVertex3f(-1.0f, 1.0f, 1.0f);    // Top Right Of The Quad (Left)
		glVertex3f(-1.0f, 1.0f,-1.0f);    // Top Left Of The Quad (Left)
		glVertex3f(-1.0f,-1.0f,-1.0f);    // Bottom Left Of The Quad (Left)
		glVertex3f(-1.0f,-1.0f, 1.0f);    // Bottom Right Of The Quad (Left)
		glColor3f(1.0f,0.0f,1.0f);    // Color Violet
		glVertex3f( 1.0f, 1.0f,-1.0f);    // Top Right Of The Quad (Right)
		glVertex3f( 1.0f, 1.0f, 1.0f);    // Top Left Of The Quad (Right)
		glVertex3f( 1.0f,-1.0f, 1.0f);    // Bottom Left Of The Quad (Right)
		glVertex3f( 1.0f,-1.0f,-1.0f);    // Bottom Right Of The Quad (Right)
	glEnd();            // End Drawi
}

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(MB_setColori_overloads, MeshBuilder::setColori, 3, 4)

BOOST_PYTHON_MODULE(test)
{	
	class_<Vector3>("Vector3_",init<float,float,float>())
		.def(self + self)
		.def(self * self)
		.def(self_ns::str(self))
		.def_readwrite("x",&Vector3::x)
		.def_readwrite("y",&Vector3::y)
		.def_readwrite("z",&Vector3::z);


	class_<MeshBuilder>("MeshBuilder",init<int>())
		.def("getInstance",&MeshBuilder::getInstance,return_value_policy<reference_existing_object>())
		.def("begin",&MeshBuilder::begin)
		.def("render",&MeshBuilder::render)
		.def("reset",&MeshBuilder::reset)
		.def("addVertex",&MeshBuilder::addVertex)
		.def("setColor",&MeshBuilder::setColor)
		.def("setColori",&MeshBuilder::setColori,MB_setColori_overloads(args("_r","_g","_b","_a")))
		.def("setNormal",&MeshBuilder::setNormal)
		.def("setTexCoord",&MeshBuilder::setTexCoord);

	def("CUBE",CUBE);
}