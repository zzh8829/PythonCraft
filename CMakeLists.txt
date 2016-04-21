cmake_minimum_required(VERSION 3.2)

project(main)

set(GEN_LIB 1)

set(CMAKE_MODULE_PATH "${CMAKE_BINARY_DIR}/cmake")

SET(HEADER_FILES
	src/Level.h
	src/World.h
	src/Region.h
	src/ChunkData.h
	src/Section.h
	src/NibbleArray.h
	src/LevelRender.h
	# src/ChunkRender.h
	src/WorldRender.h
	src/SectionRender.h
	src/QuadBuilder.h
	src/Block.h
	src/BlockRender.h
	src/Texture.h
	src/TextureManager.h
	src/NBT.h
	src/Endian.h
	src/CommonInc.h
	src/FileFinder.h
	src/Frustum.h
	src/Camera.h
	# src/Vector3.h
	# src/Quaternion.h
	# src/Matrix3.h
	# src/Matrix4.h
	src/math/Sort.h
	src/math/AABB.h
)

SET(SOURCE_FILES
	src/Level.cpp
	src/World.cpp
	src/Region.cpp
	src/ChunkData.cpp
	src/Section.cpp
	src/NibbleArray.cpp
	src/LevelRender.cpp
	# src/ChunkRender.cpp
	src/WorldRender.cpp
	src/SectionRender.cpp
	src/QuadBuilder.cpp
	src/Block.cpp
	src/BlockRender.cpp
	src/Texture.cpp
	src/TextureManager.cpp
	src/Frustum.cpp
	src/camera.cpp
	# src/Vector3.cpp
	# src/Quaternion.cpp
	# src/Matrix3.cpp
	# src/Matrix4.cpp
	src/NBT.cpp
	src/gzip.cpp
	src/zlib.cpp
	src/main.cpp
)

if(WIN32)
  SET(LIB_FILES
  	z
  	mingw32
  	user32
  	gdi32
  	winmm
  	dxguid
  )
elseif(APPLE)
  SET(LIB_FILES
  	z
  )
else()
  message(FATAL_ERROR "only suport mac and windows right now")
endif()

# =================
# External Projects
# =================
include(ExternalProject)

# BOOST

set(BoostComponents python system filesystem)
include(boost)

include_directories(${Boost_INCLUDE_DIRS})
list(APPEND LIB_FILES ${Boost_LIBRARIES})

# SDL

find_package(SDL 1.2)

if(NOT SDL_FOUND)
  message(FATAL_ERROR "SDL NOT FOUND")
endif()

include_directories(${SDL_INCLUDE_DIR})
list(APPEND LIB_FILES ${SDL_LIBRARY})

# OPENGL

find_package(OPENGL)

if(NOT OPENGL_FOUND OR NOT OPENGL_GLU_FOUND)
  message(FATAL_ERROR "OpenGL NOT FOUND")
endif()

if(APPLE)
  include_directories(${OPENGL_INCLUDE_DIR}/Headers)
else()
  include_directories(${OPENGL_INCLUDE_DIR}/GL)
endif()

list(APPEND LIB_FILES ${OPENGL_LIBRARIES})

# PNG 
find_package(PNG)

if(NOT PNG_FOUND)
  message(FATAL_ERROR "PNG NOT FOUND")
endif()

if(APPLE)
  # weird mac shit 
  include_directories("/usr/local/include/libpng16")
else()
  include_directories(${PNG_INCLUDE_DIRS})
endif()

list(APPEND LIB_FILES ${PNG_LIBRARIES})
add_definitions(${PNG_DEFINITIONS})

# PYTHON3
execute_process(COMMAND python3 -c "import sys; print('%d.%d' % (sys.version_info[0], sys.version_info[1]))" OUTPUT_VARIABLE PYTHON_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)
set(PYTHON_LIBRARIES "python${PYTHON_VERSION}")

execute_process(COMMAND python3 -c "import sys; print(sys.prefix)" OUTPUT_VARIABLE PYTHON_ROOT OUTPUT_STRIP_TRAILING_WHITESPACE)

execute_process(COMMAND python3 -c "from __future__ import print_function; import distutils.sysconfig; print(distutils.sysconfig.get_python_inc(True))" OUTPUT_VARIABLE PYTHON_INCLUDE_DIRS OUTPUT_STRIP_TRAILING_WHITESPACE)

include_directories(${PYTHON_INCLUDE_DIRS})
link_directories(${PYTHON_ROOT}/lib)
list(APPEND LIB_FILES ${PYTHON_LIBRARIES})

# =================
#       MAIN
# =================

if(GEN_LIB)
  if(APPLE)
    set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
  endif(APPLE)
  add_library(main SHARED ${SOURCE_FILES} ${HEADER_FILES} )
else()
  add_executable(main ${SOURCE_FILES} ${HEADER_FILES} )
endif()

target_compile_features(main PRIVATE cxx_range_for)
target_link_libraries(main ${LIB_FILES})
