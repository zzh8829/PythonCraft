#include "Level.h"
#include "World.h"
#include "NBT.h"
using namespace std;

Level::Level(string path,string name):
mDirectory(path+name+"/"),
mName(name)
{
	loadLevel();
}

Level::~Level()
{
	delete mWorld;
}

void Level::loadLevel()
{
	NBT::TagCompound* root = NBT::ReadNBTFromGzipFile(mDirectory+"level.dat");

	NBT::Print(cout,root);

	NBT::TagCompound* data = root->getCompound("Data");

	mWorld = new World(mDirectory+"region/");
	mWorld->loadWorld();

	NBT::TagList* pos = data->getCompound("Player")->getList("Pos");
	playerX = pos->getDouble(0);
	playerY = pos->getDouble(1);
	playerZ = pos->getDouble(2);

}

ofstream Level::logfile("E:/abc.txt");