#ifndef _TEXTUREMANAGER_H_
#define _TEXTUREMANAGER_H_

#include "CommonInc.h"
#include "Texture.h"

class TextureManager
{
public:
	TextureManager(std::string);
	virtual ~TextureManager();

	std::map<std::string, Texture* > mTexMap;	

	static TextureManager* getInstance();
	static TextureManager* initialize(std::string);
	Texture* getTexture(std::string);

	int loadPNG(std::string,int*,int*);
	void loadTextures();
	void loadTexture(std::string);
	void loadTextureCfg(std::string);
	void loadTextureTxt(std::string);

	std::string mPath;

private:
	
	static TextureManager* mTextureManager;

};

#endif
