SET( ROOTDIR "F:")

SET( CMAKE_C_COMPILER "F:/MinGW/bin/gcc.exe" )
SET( CMAKE_CXX_COMPILER "F:/MinGW/bin/g++.exe" )
SET( CMAKE_RC_COMPILER "F:/MinGW/bin/windres.exe")
SET( CMAKE_MAKE_PROGRAM "F:/MinGW/bin/make.exe")
set( CMAKE_BUILD_TYPE Release)

set( GEN_LIB 1)


cmake_minimum_required(VERSION 2.8)
project(main)

SET(LIBHOME F:/lib)

ADD_DEFINITIONS( -static-libgcc  )
ADD_DEFINITIONS( -static-libstdc++ )
ADD_DEFINITIONS( -std=c++0x )

include_directories(F:/lib/include)
include_directories(F:/lib/sdl/include)
include_directories(F:/lib/boost/include)
include_directories(F:/Python32/include)

link_directories(F:/lib/lib)
link_directories(F:/lib/sdl/lib)
link_directories(F:/lib/boost/lib)
link_directories(F:/Python32/libs)


SET(HEADER_FILE
	Level.h
	World.h
	Region.h
	ChunkData.h
	Section.h
	NibbleArray.h

	LevelRender.h
	#ChunkRender.h
	WorldRender.h
	SectionRender.h

	QuadBuilder.h

	Block.h
	BlockRender.h

	Texture.h
	TextureManager.h
	
	NBT.h

	Endian.h
	CommonInc.h

	FileFinder.h

	Frustum.h
	Camera.h

	#Vector3.h
	#Quaternion.h
	#Matrix3.h
	#Matrix4.h

	math/Sort.h
	math/AABB.h
)

SET(SOURCE_FILE
	Level.cpp
	World.cpp
	Region.cpp
	ChunkData.cpp
	Section.cpp
	NibbleArray.cpp

	LevelRender.cpp
	#ChunkRender.cpp
	WorldRender.cpp
	SectionRender.cpp

	QuadBuilder.cpp

	Block.cpp
	BlockRender.cpp

	Texture.cpp
	TextureManager.cpp

	Frustum.cpp
	camera.cpp

	#Vector3.cpp
	#Quaternion.cpp
	#Matrix3.cpp
	#Matrix4.cpp

	NBT.cpp

	gzip.cpp
	zlib.cpp

	main.cpp
)

SET(LIB_FILE
	boost_python3-mgw46-mt-1_52
	python32
	opengl32
	glu32
	z
	png
	mingw32
	SDLmain
	SDL
	user32
	gdi32
	winmm
	dxguid
)

if(GEN_LIB)

ADD_LIBRARY(main SHARED ${SOURCE_FILE} ${HEADER_FILE} )
TARGET_LINK_LIBRARIES(main ${LIB_FILE})

else()
add_executable( main
		${SOURCE_FILE}
		${HEADER_FILE}
      )
	   
TARGET_LINK_LIBRARIES( main ${LIB_FILE})

endif()