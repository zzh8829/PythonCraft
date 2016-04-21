#include "NBT.h"
using namespace std;

namespace NBT
{
	string ReadString(istream& input)
	{
		int16_t len = ReadSwap<int16_t>(input);
		if( len == 0 )
			return string("");
		char *buf = new char[len+1];
		wchar_t *wbuf = new wchar_t[len+1];
		input.read(buf,len);
		buf[len] = '\0';
		mbstowcs( wbuf , buf , len+1 );
		wstring wstr(wbuf);
		delete[] wbuf;
		delete[] buf;
		return string(wstr.begin(),wstr.end() );
	}

	TagBase *NewTag(uint8_t type,string name)
	{
		switch(type)
		{
			case 0: return new TagEnd(name); break;
			case 1: return new TagByte(name); break;
			case 2: return new TagShort(name); break;
			case 3: return new TagInt(name); break;
			case 4: return new TagLong(name); break;
			case 5: return new TagFloat(name); break;
			case 6: return new TagDouble(name); break;
			case 7: return new TagByteArray(name); break;
			case 8: return new TagString(name); break;
			case 9: return new TagList(name); break;
			case 10: return new TagCompound(name); break;
			case 11: return new TagIntArray(name); break;
			default: return new TagEnd(name);
		}
	}

	TagBase* ReadNamedTag(istream& input)
	{
		uint8_t typ = Read<uint8_t>(input);
		if(typ == 0) return NewTag(0,"");
		TagBase* tag = NewTag(typ,ReadString(input));
		tag->read(input);
		return tag;
	}

	TagCompound* ReadNBTFromZlibStream(istream& inputstream)
	{
		boost::iostreams::filtering_istream input;
		input.push(boost::iostreams::zlib_decompressor());
		input.push(inputstream);

		return (TagCompound*)ReadNamedTag(input);
	}

	TagCompound* ReadNBTFromGzipFile(string filename)
	{
		ifstream file(filename.c_str(),ios_base::in|ios_base::binary);
		boost::iostreams::filtering_istream input;
		input.push(boost::iostreams::gzip_decompressor());
		input.push(file);
		
		return (TagCompound*)ReadNamedTag(input);
	}

	TagCompound* ReadNBTFromZlibFile(string filename)
	{
		ifstream file(filename.c_str(),ios_base::in|ios_base::binary);
		boost::iostreams::filtering_istream input;
		input.push(boost::iostreams::zlib_decompressor());
		input.push(file);

		return (TagCompound*)ReadNamedTag(input);

	}

	void Print(ostream& out, TagCompound* tag, string prefix)
	{
		TagList* tmp;
		if(tag->data.size() == 0 ) 
		{
			out  << prefix << "{ }" << endl;
			return;
		}

		out << prefix << "{" << endl;
		for( TagCompound::iterator it = tag->data.begin(); it != tag->data.end(); it++ ) 
		{
			out << prefix << '\t';
			string name = it->first;
			switch( it->second->id ) {
			case TAG_Byte:
				out << "Byte " << name << " : " << int(((TagByte*)(it->second))->data) << endl;
				break;
			case TAG_Short:
				out << "Short " << name << " : " << ((TagShort*)(it->second))->data << endl;
				break;
			case TAG_Int:
				out << "Int " << name << " : " << ((TagInt*)(it->second))->data << endl;
				break;
			case TAG_Long:
				out << "Long " << name << " : " << ((TagLong*)(it->second))->data << endl;
				break;
			case TAG_Float:
				out << "Float " << name << " : " << ((TagFloat*)(it->second))->data << endl;
				break;
			case TAG_Double:
				out << "Double " << name << " : " << ((TagDouble*)(it->second))->data << endl;
				break;
			case TAG_Byte_Array:
				out << "ByteArray " << name << " size : " << ((TagByteArray*)(it->second))->data.size() << endl;
				break;
			case TAG_String:
				out << "String " << name << " : " << ((TagString*)(it->second))->data << endl;
				break;
			case TAG_List:
				tmp = (TagList*)(it->second);
				out << "List " << name << " of " << int(tmp->type) << " size : " << tmp->data.size() << endl;
				if(tmp->type == 10)
				{
					for(int i=0;i!=tmp->data.size();i++)
					{
						Print(out,(TagCompound*)(tmp->data[i]),prefix+"\t");			
					}
				}
				break;
			case TAG_Compound:
					out << "Compound " << name << endl;
					Print(out,(TagCompound*)(it->second),prefix+"\t");
					break;
			case TAG_Int_Array:
				out << "IntArray " << name << " size : " << ((TagIntArray*)(it->second))->data.size() << endl;
				break;
			default: break;
			}
		}
		out << prefix << "}" << endl ;
	}

}
