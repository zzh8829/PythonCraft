#ifndef _NBT_H_
#define _NBT_H_

#include "CommonInc.h"
#include "Endian.h"

#define BOOST_IOSTREAMS_NO_LIB

#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/filtering_stream.hpp>
#include <boost/iostreams/filtering_streambuf.hpp>
#include <boost/iostreams/filter/zlib.hpp>
#include <boost/iostreams/filter/gzip.hpp>
#include <boost/iostreams/device/file.hpp>

namespace NBT {

	enum TagType {
		TAG_End			= 0,
		TAG_Byte		= 1,
		TAG_Short		= 2,
		TAG_Int			= 3,
		TAG_Long		= 4,
		TAG_Float		= 5,
		TAG_Double		= 6,
		TAG_Byte_Array	= 7,
		TAG_String		= 8,
		TAG_List		= 9,
		TAG_Compound	= 10,
		TAG_Int_Array   = 11,
		TAG_Count       = 12
	};

	class TagBase;
	class TagEnd;
	class TagByte;
	class TagShort;
	class TagInt;
	class TagLong;
	class TagFloat;
	class TagDouble;
	class TagByteArray;
	class TagString;
	class TagList;
	class TagCompound;
	class TagIntArray;

	template <typename T>
	T Read(std::istream& input)
	{
		T data;
		input.read(reinterpret_cast<char*>(&data),sizeof(T));
		return data;
	}

	template <typename T>
	T ReadSwap(std::istream& input)
	{
		return bswap_from_big(Read<T>(input));
	}

	std::string ReadString(std::istream& input);
	TagBase *NewTag(uint8_t type,std::string name);
	TagBase* ReadNamedTag(std::istream& input);
	void Print(std::ostream& out, TagCompound* tag, std::string prefix = std::string(""));
	TagCompound* ReadNBTFromZlibStream(std::istream& inputstream);
	TagCompound* ReadNBTFromGzipFile(std::string filename);
	TagCompound* ReadNBTFromZlibFile(std::string filename);

	class TagBase
	{
	public:
		TagBase(std::string _name,uint8_t _id):name(_name),id(_id){}
		virtual ~TagBase(){}
		std::string name;
		uint8_t id;
		virtual void read(std::istream& input){}
		
	};

	class TagEnd: public TagBase
	{
	public:
		TagEnd(std::string _name):TagBase(_name,0){}

	};

	class TagByte: public TagBase
	{
	public:
		TagByte(std::string _name):TagBase(_name,1){}

		void read(std::istream& input)
		{
			data = Read<uint8_t>(input);
		}

		uint8_t data;
	};

	class TagShort: public TagBase
	{
	public:
		TagShort(std::string _name):TagBase(_name,2){}

		void read(std::istream& input)
		{
			data = ReadSwap<int16_t>(input);
		}

		int16_t data;
	};

	class TagInt: public TagBase
	{
	public:
		TagInt(std::string _name):TagBase(_name,3){}

		void read(std::istream& input)
		{
			data = ReadSwap<int32_t>(input);
		}


		int32_t data;
	};

	class TagLong: public TagBase
	{
	public:
		TagLong(std::string _name):TagBase(_name,4){}

		void read(std::istream& input)
		{
			data = ReadSwap<int64_t>(input);
		}

		int64_t data;
	};

	class TagFloat: public TagBase
	{
	public:
		TagFloat(std::string _name):TagBase(_name,5){}

		void read(std::istream& input)
		{
			data = ReadSwap<float>(input);
		}

		float data;
	};

	class TagDouble: public TagBase
	{
	public:
		TagDouble(std::string _name):TagBase(_name,6){}

		void read(std::istream& input)
		{
			data = ReadSwap<double>(input);
		}

		double data;
	};

	class TagByteArray: public TagBase
	{
	public:
		TagByteArray(std::string _name):TagBase(_name,7){}

		void read(std::istream& input)
		{
			int32_t len = ReadSwap<int32_t>(input);
			for(int i=0;i!=len;i++)
			{
				data.push_back(Read<uint8_t>(input));
			}
		}
		std::vector<uint8_t> data;
	};

	class TagString: public TagBase
	{
	public:
		TagString(std::string _name):TagBase(_name,8){}

		void read(std::istream& input)
		{
			data = ReadString(input);
		}

		std::string data;
	};


	class TagIntArray: public TagBase
	{
	public:
		TagIntArray(std::string _name):TagBase(_name,11){}

		void read(std::istream& input)
		{
			int32_t len = ReadSwap<int32_t>(input);
			for(int i=0;i!=len;i++)
			{
				data.push_back(ReadSwap<int32_t>(input));
			}
		}

		std::vector<int32_t> data;;
	};


	class TagList: public TagBase
	{
	public:
		TagList(std::string _name):TagBase(_name,9),type(0){}

		~TagList()
		{
			for(std::vector<TagBase*>::iterator it=data.begin();it!=data.end();it++)
			{
				delete (*it);
			}
			data.clear();
		}

		void read(std::istream& input)
		{

			uint8_t typ = Read<uint8_t>(input);
			type = typ;
			int32_t len = ReadSwap<int32_t>(input);
			for(int i=0;i!=len;i++)
			{
				TagBase* tag = NewTag(typ,"");
				tag->read(input);
				data.push_back(tag);
			}

		}

		size_t size()
		{
			return data.size();
		}

		inline TagCompound* getCompound(int index)
		{
			return (TagCompound*)(data[index]);
		}

		inline TagList* getList(int index)
		{
			return (TagList*)(data[index]);
		}

#define LISTGET(type,ret) \
		inline ret get##type(int index)\
		{\
			return ((Tag##type*)(data[index]))->data; \
		}

		LISTGET(Byte,int8_t)
		LISTGET(Short,int16_t)
		LISTGET(Int,int32_t)
		LISTGET(Long,int64_t)
		LISTGET(Float,float)
		LISTGET(Double,double)
		LISTGET(String,std::string)
		LISTGET(ByteArray,std::vector<uint8_t>)
		LISTGET(IntArray,std::vector<int32_t>)
	//private:
		std::vector<TagBase*> data;
		uint8_t type;
	};

	class TagCompound: public TagBase
	{
	public:
		TagCompound(std::string _name):TagBase(_name,10){}
		~TagCompound()
		{
			for(std::map<std::string,TagBase*>::iterator it=data.begin();it!=data.end();it++)
			{
				delete (it->second);
			}
			data.clear();
		}

		typedef std::map<std::string,TagBase*>::iterator iterator;

		void read(std::istream& input)
		{
			while(1)
			{
				TagBase* tag = ReadNamedTag(input);
				if(tag->id==0) break;
				data[tag->name] = tag;
			}		
		}

		inline TagCompound* getCompound(const std::string name)
		{
			return (TagCompound*)(data[name]);
		}

		inline TagList* getList(const std::string name)
		{
			return (TagList*)(data[name]);
		}


#define COMPOUNDGET(type,ret) \
		inline ret get##type(const std::string name)\
		{\
			return ((Tag##type*)(data[name]))->data; \
		}

		COMPOUNDGET(Byte,int8_t)
		COMPOUNDGET(Short,int16_t)
		COMPOUNDGET(Int,int32_t)
		COMPOUNDGET(Long,int64_t)
		COMPOUNDGET(Float,float)
		COMPOUNDGET(Double,double)
		COMPOUNDGET(String,std::string)
		COMPOUNDGET(ByteArray,std::vector<uint8_t>)
		COMPOUNDGET(IntArray,std::vector<int32_t>)
		
		std::map<std::string,TagBase*> data;
	};
	
}

#endif
