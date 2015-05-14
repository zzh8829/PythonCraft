#ifndef _LEVEL_H_
#define _LEVEL_H_

#include "CommonInc.h"
#include "World.h"

class Level
{
public:
	Level(std::string path,std::string name);
	virtual ~Level();
	void loadLevel();

	World* getWorld()
	{
		return mWorld;
	}


	int SpawnX,SpawnY,SpawnZ;

	float playerX,playerY,playerZ;


	std::string mName;

//private:
	std::string mDirectory;
	World* mWorld;
	static std::ofstream logfile;
};


#endif