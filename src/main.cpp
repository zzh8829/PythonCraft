#if defined(WIN32)
#include <windows.h>
#endif 

#include "CommonInc.h"

#include "SDL.h"

#include "Level.h"
#include "World.h"
#include "Region.h"
#include "ChunkData.h"
#include "LevelRender.h"
#include "Section.h"
#include "SectionRender.h"

#include "NBT.h"

#include "FileFinder.h"
#include "TextureManager.h"
#include "Texture.h"

#include "QuadBuilder.h"
using namespace std;

#undef main

typedef pair<int,int> Int2;

SDL_Event event;
SDL_Surface* screen;
bool isRunning = true;
bool isActive = true;

LevelRender* lr;

void SetVsync(bool s)
{
	SDL_GL_SetAttribute(SDL_GL_SWAP_CONTROL,s);
}

void glEnable2D()
{
	int vPort[4];
	glGetIntegerv(GL_VIEWPORT,vPort);
	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	glLoadIdentity();
	glOrtho( 0, vPort[2], 0, vPort[3], -1, 1);
	glMatrixMode(GL_MODELVIEW);
	glPushMatrix();
	glLoadIdentity();
	glDisable(GL_CULL_FACE);
	glClear(GL_DEPTH_BUFFER_BIT);
}

void glDisable2D()
{
	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glMatrixMode(GL_MODELVIEW);
	glPopMatrix();
}


void RenderBlockTexture(string name,int x,int y)
{
	Texture* tex = TextureManager::getInstance()->getTexture(name);
	int size = tex->size;
	//glEnable2D();
	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D,tex->id);

	QuadBuilder* mBuilder = QuadBuilder::getInstance();

	mBuilder->begin();
		mBuilder->setColori(255,255,255);
		mBuilder->setTexCoord (tex->minU, 1-tex->minV);
		mBuilder->addVertex (x, y, 0.0);
		mBuilder->setTexCoord (tex->maxU, 1-tex->minV);
		mBuilder->addVertex (x+size, y , 0.0);
		mBuilder->setTexCoord (tex->maxU, 1-tex->maxV);
		mBuilder->addVertex (x+size, y+size, 0.0);
		mBuilder->setTexCoord(tex->minU, 1-tex->maxV);
		mBuilder->addVertex (x, y+size, 0.0);
	mBuilder->render();
	//glDisable2D();
}

void InitOpenGL()
{
	glShadeModel( GL_SMOOTH );
	glClearColor( 0.0f, 0.0f, 0.0f, 0.0f );
	glClearDepth( 1.0f );
	//glEnable( GL_DEPTH_TEST );
	glDepthFunc( GL_LEQUAL );
	//glEnable(GL_ALPHA_TEST);
	glAlphaFunc( GL_GREATER, 0.5);
	//glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);

	cout << "OpenGL Version: "<< glGetString(GL_VERSION) << endl;
}

void ResizeScreen(int width,int height)
{
	if(height == 0)height = 1;
	glViewport( 0, 0, width, height );
	glMatrixMode( GL_PROJECTION );
	glLoadIdentity();
	gluPerspective( 35.0f, width/(float)height, 0.1f, 1000.0f );
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	glTranslatef(0,0,-10);
}

void UpdateScene()
{
	//lr->update(0,50,0);
}

void RenderScene()
{
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
	//glColor3f(1,1,1);
	//glLoadIdentity();


	glRotatef(0.1,1,1,1);

	//lr->render(0,50,0);
	int w,h;
	Texture* tex = TextureManager::getInstance()->getTexture("sun");
	cout << tex->id << endl;
	glEnable(GL_TEXTURE_2D);
	glBindTexture(GL_TEXTURE_2D,tex->id);
	glBegin(GL_QUADS);
	    // Front Face
	    glTexCoord2f(0.0f, 0.0f); glVertex3f(-1.0f, -1.0f,  1.0f);  // Bottom Left Of The Texture and Quad
	    glTexCoord2f(1.0f, 0.0f); glVertex3f( 1.0f, -1.0f,  1.0f);  // Bottom Right Of The Texture and Quad
	    glTexCoord2f(1.0f, 1.0f); glVertex3f( 1.0f,  1.0f,  1.0f);  // Top Right Of The Texture and Quad
	    glTexCoord2f(0.0f, 1.0f); glVertex3f(-1.0f,  1.0f,  1.0f);  // Top Left Of The Texture and Quad
	    // Back Face
	    glTexCoord2f(1.0f, 0.0f); glVertex3f(-1.0f, -1.0f, -1.0f);  // Bottom Right Of The Texture and Quad
	    glTexCoord2f(1.0f, 1.0f); glVertex3f(-1.0f,  1.0f, -1.0f);  // Top Right Of The Texture and Quad
	    glTexCoord2f(0.0f, 1.0f); glVertex3f( 1.0f,  1.0f, -1.0f);  // Top Left Of The Texture and Quad
	    glTexCoord2f(0.0f, 0.0f); glVertex3f( 1.0f, -1.0f, -1.0f);  // Bottom Left Of The Texture and Quad
	    // Top Face
	    glTexCoord2f(0.0f, 1.0f); glVertex3f(-1.0f,  1.0f, -1.0f);  // Top Left Of The Texture and Quad
	    glTexCoord2f(0.0f, 0.0f); glVertex3f(-1.0f,  1.0f,  1.0f);  // Bottom Left Of The Texture and Quad
	    glTexCoord2f(1.0f, 0.0f); glVertex3f( 1.0f,  1.0f,  1.0f);  // Bottom Right Of The Texture and Quad
	    glTexCoord2f(1.0f, 1.0f); glVertex3f( 1.0f,  1.0f, -1.0f);  // Top Right Of The Texture and Quad
	    // Bottom Face
	    glTexCoord2f(1.0f, 1.0f); glVertex3f(-1.0f, -1.0f, -1.0f);  // Top Right Of The Texture and Quad
	    glTexCoord2f(0.0f, 1.0f); glVertex3f( 1.0f, -1.0f, -1.0f);  // Top Left Of The Texture and Quad
	    glTexCoord2f(0.0f, 0.0f); glVertex3f( 1.0f, -1.0f,  1.0f);  // Bottom Left Of The Texture and Quad
	    glTexCoord2f(1.0f, 0.0f); glVertex3f(-1.0f, -1.0f,  1.0f);  // Bottom Right Of The Texture and Quad
	    // Right face
	    glTexCoord2f(1.0f, 0.0f); glVertex3f( 1.0f, -1.0f, -1.0f);  // Bottom Right Of The Texture and Quad
	    glTexCoord2f(1.0f, 1.0f); glVertex3f( 1.0f,  1.0f, -1.0f);  // Top Right Of The Texture and Quad
	    glTexCoord2f(0.0f, 1.0f); glVertex3f( 1.0f,  1.0f,  1.0f);  // Top Left Of The Texture and Quad
	    glTexCoord2f(0.0f, 0.0f); glVertex3f( 1.0f, -1.0f,  1.0f);  // Bottom Left Of The Texture and Quad
	    // Left Face
	    glTexCoord2f(0.0f, 0.0f); glVertex3f(-1.0f, -1.0f, -1.0f);  // Bottom Left Of The Texture and Quad
	    glTexCoord2f(1.0f, 0.0f); glVertex3f(-1.0f, -1.0f,  1.0f);  // Bottom Right Of The Texture and Quad
	    glTexCoord2f(1.0f, 1.0f); glVertex3f(-1.0f,  1.0f,  1.0f);  // Top Right Of The Texture and Quad
	    glTexCoord2f(0.0f, 1.0f); glVertex3f(-1.0f,  1.0f, -1.0f);  // Top Left Of The Texture and Quad
	glEnd();
	

	SDL_GL_SwapBuffers();
}

// void recFolder(string name)
// {
// 	FileFinder fd(name);
// 	string file = fd.filename();
// 	cout << file << endl;
// 	while(file!="")
// 	{
// 		if(fd.isSubDir())
// 		{
// 			recFolder(file);
// 		}
// 		cout << FileFinder::fileBaseName(file) << endl;
// 		file = fd.next();
// 	}
// }

int main(int argc, char* argv[])
{
	SDL_Init(SDL_INIT_EVERYTHING);
	SDL_WM_SetCaption("cppgame window",0);
	SetVsync(false);

	//cout << FileFinder::exists("F:/fuck") << endl; 
	//cout << FileFinder::exists("F:/PythonCraft") << endl;
	//recFolder("F:/PythonCraft/level/");
	
	
	screen = SDL_SetVideoMode(854,480,32,
		SDL_OPENGL|SDL_GL_DOUBLEBUFFER|SDL_HWSURFACE|SDL_RESIZABLE);
	InitOpenGL();

	TextureManager* t  = TextureManager::initialize("textures");

	//ResizeScreen(854,480);

	Level* l = new Level("saves/", "house");

	lr = new LevelRender(l);
	
	while(isRunning)
	{
		while(SDL_PollEvent(&event))
		{
			switch(event.type)
			{
			case SDL_ACTIVEEVENT:
				if ( event.active.gain == 0 )
					isActive = false;
				else
					isActive = true;
				break;
			case SDL_VIDEORESIZE:
				screen = SDL_SetVideoMode(event.resize.w,event.resize.h,
							16, screen->flags );
				ResizeScreen( event.resize.w, event.resize.h );
				break;
			case SDL_KEYDOWN:
				break;
			case SDL_QUIT:
				isRunning = false;
				break;
			}
		}
		//if(isActive)
		{
			UpdateScene();
			RenderScene();
		}
	}
	SDL_Quit();
	return 0;
}

#define BOOST_PYTHON_STATIC_LIB

#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
using namespace boost::python;

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(QB_begin_overloads, QuadBuilder::begin, 0,2)
BOOST_PYTHON_MODULE(libmain)
{

	def("SetVsync",&SetVsync);
	def("RenderBlockTexture",&RenderBlockTexture);

	class_< pair<int, int> >("Int2")
	    .def_readwrite("first", &std::pair<int, int>::first)
	    .def_readwrite("second", &std::pair<int, int>::second);

	class_< vector< pair<int,int> > >("VInt2")
		.def(vector_indexing_suite< vector< pair<int,int> > >());

	class_<ChunkData>("CChunkData",init< pair<int,int> >())
		.def(init<>())
		.def("getBlockId",&ChunkData::getBlockId)
		.def("setBlockId",&ChunkData::setBlockId);
	class_<World>("CWorld",init<string>())
		.def("getChunkData",&World::getChunkData,return_value_policy<reference_existing_object>())
		.def("getBlockId",&World::getBlockId)
		.def("setBlockId",&World::setBlockId)
		.def("deleteRegion",&World::deleteRegion)
		.def("deleteChunkData",&World::deleteChunkData)
		.def("getLoadedRegions",&World::getLoadedRegions);
	class_<Level>("CLevel",init<string,string>())
		.def("getWorld",&Level::getWorld,return_value_policy<reference_existing_object>())
		.def_readwrite("playerX",&Level::playerX)
		.def_readwrite("playerY",&Level::playerY)
		.def_readwrite("playerZ",&Level::playerZ);
	class_<LevelRender>("CLevelRender",init<Level*>())
		.def("update",&LevelRender::update)
		.def("render",&LevelRender::render)
		.def("getWorldRender",&LevelRender::getWorldRender,return_value_policy<reference_existing_object>());
	class_<WorldRender>("CWorldRender",init<Level*,LevelRender*>())
		.def("setViewDistance",&WorldRender::setViewDistance);
	class_<SectionRender>("CSectionRender",init<Level*>())
		.def("setPosition",&SectionRender::setPosition)
		.def("update",&SectionRender::update)
		.def("render",&SectionRender::render);
		
	class_<Texture>("CTexture")
		.def_readonly("id",&Texture::id)
		.def_readonly("width",&Texture::width)
		.def_readonly("height",&Texture::height)
		.def_readonly("size",&Texture::size)
		.def_readonly("minU",&Texture::minU)
		.def_readonly("maxU",&Texture::maxU)
		.def_readonly("minV",&Texture::minV)
		.def_readonly("maxV",&Texture::maxV)
		.def("getInterpolatedU",&Texture::getInterpolatedU)
		.def("getInterpolatedV",&Texture::getInterpolatedV);
		
	class_<TextureManager>("CTextureManager",no_init)
		.def("initialize",&TextureManager::initialize,return_value_policy<reference_existing_object>())
		.def("getInstance",&TextureManager::getInstance,return_value_policy<reference_existing_object>())
		.def("getTexture",&TextureManager::getTexture,return_value_policy<reference_existing_object>());

	void    (QuadBuilder::*qbbegin)() = &QuadBuilder::begin;

	class_<QuadBuilder>("CQuadBuilder",no_init)
		.def("getInstance",&QuadBuilder::getInstance,return_value_policy<reference_existing_object>())
		.def("addVertex",&QuadBuilder::addVertex)
		.def("addVertexWithUV",&QuadBuilder::addVertexWithUV)
		.def("addColor",&QuadBuilder::setColor)
		.def("begin",qbbegin)
		.def("render",&QuadBuilder::render);
		
}
//#include "K:/lib/boost/boost_1_52_0/libs/python/test/module_tail.cpp"
