#ifndef _ENDIAN_H_
#define _ENDIAN_H_

#include "SDL.h"
#include "SDL_endian.h"

namespace {

  // Swap BE <-> LE
   // You don't want to use these.

template<class T>
inline static
T
bswap(T); // Don't remove this, prevents dangerous implicit casts

inline static
uint16_t
bswap(uint16_t x)
{ return SDL_Swap16(x); }

inline static
int16_t
bswap(int16_t x)
{ return int16_t(bswap(uint16_t(x))); }

inline static
uint32_t
bswap(uint32_t x)
{ return SDL_Swap32(x); }

inline static
int32_t
bswap(int32_t x)
{ return int32_t(bswap(uint32_t(x))); }

inline static
uint64_t
bswap(uint64_t x)
{ return SDL_Swap64(x); }

inline static
int64_t
bswap(int64_t x)
{ return int64_t(bswap(uint64_t(x))); }

inline static
float
bswap(float x)
{ 	
	uint8_t* tmp = reinterpret_cast<uint8_t*>(&x);
	std::reverse(tmp,tmp+sizeof(float));
	return x;
}

inline static 
double
bswap(double x)
{
	uint8_t* tmp = reinterpret_cast<uint8_t*>(&x);
	std::reverse(tmp,tmp+sizeof(double));
	return x;
}

  // Swap from/to Big Endian

template<class T>
inline static
T 
bswap_from_big(T x)
{
#if SDL_BYTEORDER == SDL_BIG_ENDIAN
  return x;
#elif SDL_BYTEORDER == SDL_LIL_ENDIAN
  return bswap(x);
#else
# error: SDL endian fail.
#endif
}

template<class T>
inline static
T
bswap_to_big(T x)
{ return bswap_from_big(x); }

} // <anonymous>

#endif // _ENDIAN_H_
