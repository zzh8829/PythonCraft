cmake_minimum_required(VERSION 3.2)
project(main)

set(CMAKE_MODULE_PATH "${CMAKE_BINARY_DIR}/cmake")

# # SET( ROOTDIR "F:")

# # SET( CMAKE_C_COMPILER "F:/MinGW/bin/gcc.exe" )
# # SET( CMAKE_CXX_COMPILER "F:/MinGW/bin/g++.exe" )
# # SET( CMAKE_RC_COMPILER "F:/MinGW/bin/windres.exe")
# # SET( CMAKE_MAKE_PROGRAM "F:/MinGW/bin/make.exe")
# # set( CMAKE_BUILD_TYPE Release)

# set( GEN_LIB 1)


# SET(LIBHOME F:/lib)

# ADD_DEFINITIONS( -static-libgcc  )
# ADD_DEFINITIONS( -static-libstdc++ )
# ADD_DEFINITIONS( -std=c++11 )

# include_directories(F:/lib/include)
# include_directories(F:/lib/sdl/include)
# include_directories(F:/Python32/include)

# link_directories(F:/lib/lib)
# link_directories(F:/lib/sdl/lib)
# link_directories(F:/Python32/libs)

# =================
# External Projects
# =================
include(ExternalProject)

set(BoostComponents python)
include(boost)
include_directories("${Boost_INCLUDE_DIRS}")



# include(cmake/sdl)

# SET(HEADER_FILES
# 	Level.h
# 	World.h
# 	Region.h
# 	ChunkData.h
# 	Section.h
# 	NibbleArray.h

# 	LevelRender.h
# 	#ChunkRender.h
# 	WorldRender.h
# 	SectionRender.h

# 	QuadBuilder.h

# 	Block.h
# 	BlockRender.h

# 	Texture.h
# 	TextureManager.h
	
# 	NBT.h

# 	Endian.h
# 	CommonInc.h

# 	FileFinder.h

# 	Frustum.h
# 	Camera.h

# 	#Vector3.h
# 	#Quaternion.h
# 	#Matrix3.h
# 	#Matrix4.h

# 	math/Sort.h
# 	math/AABB.h
# )

# SET(SOURCE_FILES
# 	Level.cpp
# 	World.cpp
# 	Region.cpp
# 	ChunkData.cpp
# 	Section.cpp
# 	NibbleArray.cpp

# 	LevelRender.cpp
# 	#ChunkRender.cpp
# 	WorldRender.cpp
# 	SectionRender.cpp

# 	QuadBuilder.cpp

# 	Block.cpp
# 	BlockRender.cpp

# 	Texture.cpp
# 	TextureManager.cpp

# 	Frustum.cpp
# 	camera.cpp

# 	#Vector3.cpp
# 	#Quaternion.cpp
# 	#Matrix3.cpp
# 	#Matrix4.cpp

# 	NBT.cpp

# 	gzip.cpp
# 	zlib.cpp

# 	main.cpp
# )

# elseif(WIN32)
#   SET(LIB_FILES
#   	python34
#   	opengl32
#   	glu32
#   	z
#   	png
#   	mingw32
#   	SDLmain
#   	SDL
#   	user32
#   	gdi32
#   	winmm
#   	dxguid
#   )
# elseif(APPLE)
#   SET(LIB_FILES
#   	python34
#   	opengl32
#   	glu32
#   	z
#   	png
#   	SDLmain
#   	SDL
#   )
# else()
  
# endif()



# if(GEN_LIB)

# ADD_LIBRARY(main SHARED ${SOURCE_FILES} ${HEADER_FILES} )
# TARGET_LINK_LIBRARIES(main ${LIB_FILES} ${Boost_LIBRARIES})

# else()

# ADD_EXECUTABLE( main
# 		${SOURCE_FILES}
# 		${HEADER_FILES}
#       )
	   
# TARGET_LINK_LIBRARIES( main ${LIB_FILES} ${Boost_LIBRARIES})

# # target_link_libraries(cppbach libmidifile libportmidi librtmidi ${CORE_MIDI} ${CORE_AUDIO} ${CORE_FOUNDATION})

# endif()

