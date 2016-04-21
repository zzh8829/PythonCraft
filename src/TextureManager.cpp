#include "TextureManager.h"
#include "png.h"
#include "boost/filesystem.hpp"
#include "FileFinder.h"
#include "sdl_opengl.h"
using namespace std;
using namespace boost;

TextureManager::TextureManager(string path):
mPath(path)
{
	loadTextures();
}

TextureManager::~TextureManager()
{
	for(map<string,Texture*>::iterator it = mTexMap.begin();it!=mTexMap.end();it++)
	{
		delete it->second;
	}
	mTexMap.clear();
}

TextureManager* TextureManager::initialize(string name)
{
	if(mTextureManager)
	{
		cout << "YOU ALREADY INITIALIZED TEXTUREMANAGER";
		exit(1);;
	}
	mTextureManager = new TextureManager(name);
	return mTextureManager;
}

TextureManager* TextureManager::getInstance()
{
	if(!mTextureManager)
	{
		cout << "YOU HAVE TO INITIALIZE TEXTUREMANAGER FIRST";
		exit(1);;
		mTextureManager = new TextureManager("textures/");
	}
	return mTextureManager;
}

Texture* TextureManager::getTexture(string name)
{
	if(mTexMap.find(name)==mTexMap.end())
	{
		return 0;
	}
	//if(name == "missingno")name = "dirt";
	//cout <<"getTexture: " << name << " ID: " << mTexMap[name]->id << endl; 
	return mTexMap[name];
}

void loadTextureRec(TextureManager* tm, filesystem::path dir_path)
{
  if ( !filesystem::exists( dir_path ) ) return;
  filesystem::directory_iterator end_itr; // default construction yields past-the-end
  for ( filesystem::directory_iterator itr( dir_path );
        itr != end_itr;
        ++itr )
  {
    if(is_directory(itr->status()) )
    {
      loadTextureRec(tm, itr->path());
    }
    else if ( itr->path().extension() == ".png" ) // see below
    {
    	string file = itr->path().string();
    	tm->loadTexture(file);
    	if(filesystem::exists(file + ".cfg"))
    	{
    		tm->loadTextureCfg(file);
    	}
    	else if(filesystem::exists(file + ".txt"))
    	{
    		tm->loadTextureTxt(file);
    	}
    }
  }
}

void TextureManager::loadTextures()
{
	loadTextureRec(this, filesystem::path(mPath));
}


// void TextureManager::loadTextureRec(string name)
// {
// 	load_helper(path(name));

// 	FileFinder fd(name);
// 	string file = fd.filename();
// 	while(file!="")
// 	{
// 		if(fd.isSubDir())
// 		{
// 			loadTextureRec(file);
// 		}
// 		if(FileFinder::endswith(file,".png"))
// 		{
			
// 			if(FileFinder::exists(file+".cfg"))
// 			{
// 				loadTextureCfg(file);
// 			} 
// 			else if (FileFinder::exists(file+".txt"))
// 			{
// 				loadTextureTxt(file);
// 			}
// 		}
// 		file = fd.next();
// 	}
// }

int GetTextureInfo(int ColourType)
{
	int ret;
	switch(ColourType)
	{
		case PNG_COLOR_TYPE_GRAY:
			ret = 1;
		break;
		case PNG_COLOR_TYPE_GRAY_ALPHA:
			ret = 2;
		break;
		case PNG_COLOR_TYPE_RGB:
			ret = 3;
		break;
		case PNG_COLOR_TYPE_RGB_ALPHA:
			ret = 4;
		break;
		default:
			ret = -1;//fucked
	};
	return ret;
};

int TextureManager::loadPNG(string name,int* owidth,int* oheight)
{
	GLuint texture;
	png_structp png_ptr = NULL;
	png_infop info_ptr = NULL;
	png_bytep *row_pointers = NULL;
	int bitDepth, colourType;

	FILE *pngFile = fopen(name.c_str(), "rb");

	if(!pngFile)
		return 0;

	png_byte sig[8];

	fread(&sig, 8, sizeof(png_byte), pngFile);
	rewind(pngFile);//so when we init io it won't bitch
	if(!png_check_sig(sig, 8))
		return 0;

	png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL,NULL,NULL);

	if(!png_ptr)
		return 0;

	if(setjmp(png_jmpbuf(png_ptr)))
		return 0;

	info_ptr = png_create_info_struct(png_ptr);

	if(!info_ptr)
		return 0;

	png_init_io(png_ptr, pngFile);

	png_read_info(png_ptr, info_ptr);

	bitDepth = png_get_bit_depth(png_ptr, info_ptr);

	colourType = png_get_color_type(png_ptr, info_ptr);

	if(colourType == PNG_COLOR_TYPE_PALETTE)
		png_set_palette_to_rgb(png_ptr);
	else if(colourType == PNG_COLOR_TYPE_GRAY && bitDepth < 8)
		png_set_expand_gray_1_2_4_to_8(png_ptr);

	if(png_get_valid(png_ptr, info_ptr, PNG_INFO_tRNS))
		png_set_tRNS_to_alpha(png_ptr);

	if(bitDepth == 16)
		png_set_strip_16(png_ptr);
	else if(bitDepth < 8)
		png_set_packing(png_ptr);

	png_read_update_info(png_ptr, info_ptr);

	png_uint_32 width, height;
	png_get_IHDR(png_ptr, info_ptr, &width, &height,
			&bitDepth, &colourType, NULL, NULL, NULL);

	int components;

	switch(colourType)
	{
		case PNG_COLOR_TYPE_GRAY:
			components = 1;
		break;
		case PNG_COLOR_TYPE_GRAY_ALPHA:
			components = 2;
		break;
		case PNG_COLOR_TYPE_RGB:
			components = 3;
		break;
		case PNG_COLOR_TYPE_RGB_ALPHA:
			components = 4;
		break;
		default:
			if(png_ptr)
				png_destroy_read_struct(&png_ptr, &info_ptr, NULL);
			return 0;
	}

	GLubyte *pixels = (GLubyte *)malloc(sizeof(GLubyte) * (width * height * components));

	row_pointers = (png_bytep *)malloc(sizeof(png_bytep) * height);

	for(int i = 0; i < height; ++i)
		row_pointers[i] = (png_bytep)(pixels + (i * width * components));
	//for(int i= height-1;i>=0;i--)
		//row_pointers[height-i-1] = (png_bytep)(pixels + (i * width * components));

	png_read_image(png_ptr, row_pointers);
	png_read_end(png_ptr, NULL);


	glGenTextures(1, &texture);
	glBindTexture(GL_TEXTURE_2D, texture);
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	GLuint glcolours;
	(components==4) ? (glcolours = GL_RGBA): (0);
	(components==3) ? (glcolours = GL_RGB): (0);
	(components==2) ? (glcolours = GL_LUMINANCE_ALPHA): (0);
	(components==1) ? (glcolours = GL_LUMINANCE): (0);

	glTexImage2D(GL_TEXTURE_2D, 0, components, width, height, 0, glcolours, GL_UNSIGNED_BYTE, pixels);

	png_destroy_read_struct(&png_ptr, &info_ptr, NULL);

	fclose(pngFile);
	free(row_pointers);
	free(pixels);

	*owidth = width;
	*oheight = height;
	return texture;	
}

void TextureManager::loadTexture(string name)
{
	//cout << "Load Texture: " << name << endl;
	int width,height;
	Texture* tex = new Texture();
	tex->id = loadPNG(name,&width,&height);
	tex->width = width;
	tex->height = height;
	tex->minU = 0;
	tex->maxU = 1;
	tex->minV = 0;
	tex->maxV = 1;
	mTexMap[FileFinder::fileBaseName(name)] = tex;
}

void TextureManager::loadTextureCfg(string name)
{
	cout << "Load Texture with Config: " << name << endl;
	int width,height;
	int id = loadPNG(name,&width,&height);
	ifstream file((name+".cfg").c_str());
	string texname;
	float minu,minv,maxu,maxv;
	int orgx,orgy;
	int size;
	string rot;
	while((file >> texname))
	{
		file >> minu >> maxu >> minv >> maxv >> size >> rot >> orgx >> orgy;
		Texture* tex = new Texture();
		tex->id = id;
		tex->minU = minu;
		tex->maxU = maxu;
		tex->minV = minv;
		tex->maxV = maxv;
		tex->size = size;
		mTexMap[texname]=tex;
	}
	file.close();
}

void TextureManager::loadTextureTxt(string name)
{
	cout << "Load Texture with Txt: " << name << endl;
	ifstream file((name+".txt").c_str());
	file.close();

}

TextureManager* TextureManager::mTextureManager = 0;
