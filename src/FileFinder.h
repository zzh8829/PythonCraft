#ifndef _FILEFINDER_H_
#define _FILEFINDER_H_

#include "CommonInc.h"

#if defined(_WIN64) || defined(_WIN32)

#include <windows.h>

class FileFinder 
{
public:
	inline explicit FileFinder(std::string dirname)
	{
		path = dirname;
		if(path[path.size()-1]!='\\' && path[path.size()-1]!='/')
		{
			path += "/";
		}
		handle_ = FindFirstFileA((path+"*.*").c_str(),&data_);
	}

	inline ~FileFinder()
	{ 
		close(); 
	}

	static bool endswith(std::string str,std::string end)
	{
		if(str.size() >= end.size())
		{
			return str.compare(str.size()-end.size(),end.size(),end)==0;
		}
		return false;
	}

	static bool exists(std::string name)
	{
		return GetFileAttributesA(name.c_str())!=INVALID_FILE_ATTRIBUTES;
	}

	static std::string fileBaseName(std::string name)
	{
		int dpos=name.size();
		while(dpos>0 && name[--dpos]!='.');
		int spos=dpos;
		while(spos>0 && (name[--spos]!='\\' && name[spos]!='/'));
		//std::cout << name << " " << dpos <<" " << spos << " "<< std::endl;
		return name.substr(spos+1,dpos-spos-1);
	}

	void close()
	{
		if (handle_ == INVALID_HANDLE_VALUE)
			return;
		FindClose(handle_);
		handle_ = INVALID_HANDLE_VALUE;
	}

	inline bool isDir() const
	{ 
		return (data_.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0; 
	}

	inline bool isSubDir() const 
	{
		return (data_.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0 && data_.cFileName[0]!='.';
	}

	inline std::string filename() const
	{
		return handle_ != INVALID_HANDLE_VALUE ? path+std::string(data_.cFileName) : ""; 
	}

	inline std::string next()
	{
		if (FindNextFileA(handle_, &data_) != FALSE)
			return path+std::string(data_.cFileName);
		close();
		return "";
	}


private:
	FileFinder(const FileFinder&);
	FileFinder& operator=(const FileFinder&);

	WIN32_FIND_DATAA data_;
	HANDLE handle_;

	std::string path;
};

#else

class FileFinder 
{
public:
	static bool endswith(std::string str,std::string end)
	{
		if(str.size() >= end.size())
		{
			return str.compare(str.size()-end.size(),end.size(),end)==0;
		}
		return false;
	}

	static std::string fileBaseName(std::string name)
	{
		int dpos=name.size();
		while(dpos>0 && name[--dpos]!='.');
		int spos=dpos;
		while(spos>0 && (name[--spos]!='\\' && name[spos]!='/'));
		//std::cout << name << " " << dpos <<" " << spos << " "<< std::endl;
		return name.substr(spos+1,dpos-spos-1);
	}
};

#endif

#endif
