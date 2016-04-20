# modified from maidsafe cmake_module/add_boost.cmake

set(BoostVersion 1.60.0)
set(BoostSHA1 7f56ab507d3258610391b47fef6b11635861175a)

set(Boost_USE_STATIC_LIBS ON) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME ON) 
find_package(Boost ${BoostVersion} COMPONENTS ${BoostComponents}) 

macro(_BOOST_FOUND Component)
  if(NOT Boost_${Component}_FOUND)
    message(STATUS "Could NOT find Boost ${Component}")
    set(Boost_FOUND OFF)
  endif()
endmacro()

foreach(BoostComponent ${BoostComponents})
  _BOOST_FOUND(${BoostComponents})
endforeach()

if(Boost_FOUND)
  message("Boost Found: " ${Boost_INCLUDE_DIRS} ${Boost_LIBRARIES})
  return()
endif()

# Download and Build Boost

# Create build folder name derived from version
string(REGEX REPLACE "beta\\.([0-9])$" "beta\\1" BoostFolderName ${BoostVersion})
string(REPLACE "." "_" BoostFolderName ${BoostFolderName})
set(BoostFolderName boost_${BoostFolderName})

# Set up boost directory
set(BoostCacheDir "${CMAKE_BINARY_DIR}/lib/boost")
file(MAKE_DIRECTORY "${BoostCacheDir}")

# Set up the full path to the source directory
set(BoostSourceDir "${BoostFolderName}_${CMAKE_CXX_COMPILER_ID}_${CMAKE_CXX_COMPILER_VERSION}")

string(REPLACE "." "_" BoostSourceDir ${BoostSourceDir})
set(BoostSourceDir "${BoostCacheDir}/${BoostSourceDir}")

# Download boost if required
set(ZipFilePath "${BoostCacheDir}/${BoostFolderName}.tar.bz2")
if(NOT EXISTS ${ZipFilePath})
  message(STATUS "Downloading boost ${BoostVersion} to ${BoostCacheDir}")
endif()
file(DOWNLOAD http://sourceforge.net/projects/boost/files/boost/${BoostVersion}/${BoostFolderName}.tar.bz2/download
     ${ZipFilePath}
     STATUS Status
     SHOW_PROGRESS
     EXPECTED_HASH SHA1=${BoostSHA1}
     )

# Extract boost if required
string(FIND "${Status}" "returning early" Found)
if(Found LESS "0" OR NOT IS_DIRECTORY "${BoostSourceDir}")
  set(BoostExtractFolder "${BoostCacheDir}/boost_unzip")
  file(REMOVE_RECURSE ${BoostExtractFolder})
  file(MAKE_DIRECTORY ${BoostExtractFolder})
  file(COPY ${ZipFilePath} DESTINATION ${BoostExtractFolder})
  message(STATUS "Extracting boost ${BoostVersion} to ${BoostExtractFolder}")
  execute_process(COMMAND ${CMAKE_COMMAND} -E tar xfz ${BoostFolderName}.tar.bz2
                  WORKING_DIRECTORY ${BoostExtractFolder}
                  RESULT_VARIABLE Result
                  )
  if(NOT Result EQUAL "0")
    message(FATAL_ERROR "Failed extracting boost ${BoostVersion} to ${BoostExtractFolder}")
  endif()
  file(REMOVE ${BoostExtractFolder}/${BoostFolderName}.tar.bz2)

  # Get the path to the extracted folder
  file(GLOB ExtractedDir "${BoostExtractFolder}/*")
  list(LENGTH ExtractedDir n)
  if(NOT n EQUAL "1" OR NOT IS_DIRECTORY ${ExtractedDir})
    message(FATAL_ERROR "Failed extracting boost ${BoostVersion} to ${BoostExtractFolder}")
  endif()
  file(RENAME ${ExtractedDir} ${BoostSourceDir})
  file(REMOVE_RECURSE ${BoostExtractFolder})
endif()

# Build b2 (bjam) if required
unset(b2Path CACHE)
find_program(b2Path NAMES b2 PATHS ${BoostSourceDir} NO_DEFAULT_PATH)
if(NOT b2Path)
  message(STATUS "Building b2 (bjam)")
  if(MSVC)
    set(b2Bootstrap "bootstrap.bat")
  else()
    set(b2Bootstrap "./bootstrap.sh")
    if(CMAKE_CXX_COMPILER_ID MATCHES "^(Apple)?Clang$")
      list(APPEND b2Bootstrap --with-toolset=clang)
    elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
      list(APPEND b2Bootstrap --with-toolset=gcc)
    endif()
  endif()
  execute_process(COMMAND ${b2Bootstrap} WORKING_DIRECTORY ${BoostSourceDir}
                  RESULT_VARIABLE Result OUTPUT_VARIABLE Output ERROR_VARIABLE Error)
  if(NOT Result EQUAL "0")
    message(FATAL_ERROR "Failed running ${b2Bootstrap}:\n${Output}\n${Error}\n")
  endif()
endif()
file(MAKE_DIRECTORY "${BoostCacheDir}/build")

# Set up general b2 (bjam) command line arguments
set(b2Args <SOURCE_DIR>/b2
           link=static
           threading=multi
           runtime-link=static
           --build-dir=build
           stage
           -d+2
           --hash
           )

if(CMAKE_BUILD_TYPE STREQUAL "Release")
  list(APPEND b2Args variant=release)
endif()

# Set up platform-specific b2 (bjam) command line arguments
if(MSVC)
  if(MSVC11)
    list(APPEND b2Args toolset=msvc-11.0)
  elseif(MSVC12)
    list(APPEND b2Args toolset=msvc-12.0)
  elseif(MSVC14)
    list(APPEND b2Args toolset=msvc-14.0)
  endif()
  list(APPEND b2Args
              define=_BIND_TO_CURRENT_MFC_VERSION=1
              define=_BIND_TO_CURRENT_CRT_VERSION=1
              --layout=versioned
              )
  if(TargetArchitecture STREQUAL "x86_64")
    list(APPEND b2Args address-model=64)
  endif()
elseif(APPLE)
  list(APPEND b2Args toolset=clang cxxflags=-fPIC cxxflags=-std=c++11 cxxflags=-stdlib=libc++ linkflags=-stdlib=libc++ architecture=combined address-model=32_64 --layout=tagged)
elseif(UNIX)
  list(APPEND b2Args --layout=tagged -sNO_BZIP2=1) 
  list(APPEND b2Args cxxflags=-fPIC cxxflags=-std=c++11)
  # Need to configure the toolset based on whatever version CMAKE_CXX_COMPILER is
  string(REGEX MATCH "[0-9]+\\.[0-9]+" ToolsetVer "${CMAKE_CXX_COMPILER_VERSION}")
  if(CMAKE_CXX_COMPILER_ID MATCHES "^(Apple)?Clang$")
    list(APPEND b2Args toolset=clang-${ToolsetVer})
  elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    list(APPEND b2Args toolset=gcc-${ToolsetVer})
  endif()
endif()

# Get list of components
execute_process(COMMAND ./b2 --show-libraries WORKING_DIRECTORY ${BoostSourceDir}
                ERROR_QUIET OUTPUT_VARIABLE Output)
string(REGEX REPLACE "(^[^:]+:|[- ])" "" BoostAvailableComponents "${Output}")
string(REGEX REPLACE "\n" ";" BoostAvailableComponents "${BoostAvailableComponents}")

function(underscores_to_camel_case VarIn VarOut)
  string(REPLACE "_" ";" Pieces ${VarIn})
  foreach(Part ${Pieces})
    string(SUBSTRING ${Part} 0 1 Initial)
    string(SUBSTRING ${Part} 1 -1 Part)
    string(TOUPPER ${Initial} Initial)
    set(CamelCase ${CamelCase}${Initial}${Part})
  endforeach()
  set(${VarOut} ${CamelCase} PARENT_SCOPE)
endfunction()

# Build each required component
include(ExternalProject)
foreach(Component ${BoostComponents})
  if(NOT ";${BoostAvailableComponents};" MATCHES "${Component}")
    message(FATAL_ERROR "Could NOT find Boost ${Component} in ${BoostSourceDir}")
  endif()

  # hanle wrong inlcude directory in mac homebrew python 
  if(APPLE AND (Component STREQUAL "python"))
    execute_process(COMMAND python -c "from __future__ import print_function; import distutils.sysconfig; print(distutils.sysconfig.get_python_inc(True))" OUTPUT_VARIABLE PYINCLUDE OUTPUT_STRIP_TRAILING_WHITESPACE)

    list(APPEND b2Args cxxflags=-I${PYINCLUDE})
  endif()

  ExternalProject_Add(
    boost_${Component}
    PREFIX ${BoostCacheDir}/build
    SOURCE_DIR ${BoostSourceDir}
    BINARY_DIR ${BoostSourceDir}
    CONFIGURE_COMMAND ""
    BUILD_COMMAND "${b2Args}" --with-${Component}
    INSTALL_COMMAND ""
    LOG_BUILD ON
    )
  
  if(Component STREQUAL "test")
    set(ComponentLibName unit_test_framework)
  else()
    set(ComponentLibName ${Component})
  endif()

  underscores_to_camel_case(${Component} CamelCaseComponent)
  add_library(Boost${CamelCaseComponent} STATIC IMPORTED GLOBAL)
  
  if(MSVC)
    if(MSVC11)
      set(CompilerName vc110)
    elseif(MSVC12)
      set(CompilerName vc120)
    elseif(MSVC14)
      set(CompilerName vc140)
    endif()
    string(REGEX MATCH "[0-9]_[0-9][0-9]" Version "${BoostFolderName}")
    set_target_properties(Boost${CamelCaseComponent} PROPERTIES
                          IMPORTED_LOCATION_DEBUG ${BoostSourceDir}/stage/lib/libboost_${ComponentLibName}-${CompilerName}-mt-gd-${Version}.lib
                          IMPORTED_LOCATION_MINSIZEREL ${BoostSourceDir}/stage/lib/libboost_${ComponentLibName}-${CompilerName}-mt-${Version}.lib
                          IMPORTED_LOCATION_RELEASE ${BoostSourceDir}/stage/lib/libboost_${ComponentLibName}-${CompilerName}-mt-${Version}.lib
                          IMPORTED_LOCATION_RELWITHDEBINFO ${BoostSourceDir}/stage/lib/libboost_${ComponentLibName}-${CompilerName}-mt-${Version}.lib
                          IMPORTED_LOCATION_RELEASENOINLINE ${BoostSourceDir}/stage/lib/libboost_${ComponentLibName}-${CompilerName}-mt-${Version}.lib
                          LINKER_LANGUAGE CXX)
  else()
    set_target_properties(Boost${CamelCaseComponent} PROPERTIES
                          IMPORTED_LOCATION ${BoostSourceDir}/stage/lib/libboost_${ComponentLibName}-mt-s.a
                          LINKER_LANGUAGE CXX)
  endif()
  set(Boost${CamelCaseComponent}Libs Boost${CamelCaseComponent})
  if(Component STREQUAL "locale")
    if(APPLE)
      find_library(IconvLib iconv)
      if(NOT IconvLib)
        message(FATAL_ERROR "libiconv.dylib must be installed to a standard location.")
      endif()
      set(Boost${CamelCaseComponent}Libs Boost${CamelCaseComponent} ${IconvLib})
    elseif(UNIX)
      if(BSD)
        find_library(IconvLib libiconv.a)
        if(NOT IconvLib)
          set(Msg "libiconv.a must be installed to a standard location.")
          set(Msg "  For ${Msg} on FreeBSD 10 or later, run\n  pkg install libiconv")
          message(FATAL_ERROR "${Msg}")
        endif()
        set(Boost${CamelCaseComponent}Libs Boost${CamelCaseComponent} ${IconvLib})
      elseif(NOT ANDROID_BUILD)
        find_library(Icui18nLib libicui18n.a)
        find_library(IcuucLib libicuuc.a)
        find_library(IcudataLib libicudata.a)
        if(NOT Icui18nLib OR NOT IcuucLib OR NOT IcudataLib)
          set(Msg "libicui18n.a, libicuuc.a & licudata.a must be installed to a standard location.")
          set(Msg "  For ${Msg} on Ubuntu/Debian, run\n  sudo apt-get install libicu-dev")
          message(FATAL_ERROR "${Msg}")
        endif()
        set(Boost${CamelCaseComponent}Libs Boost${CamelCaseComponent} ${Icui18nLib} ${IcuucLib} ${IcudataLib})
      endif()
    else()
      set(Boost${CamelCaseComponent}Libs Boost${CamelCaseComponent})
    endif()
  endif()
  list(APPEND Boost_LIBRARIES Boost${CamelCaseComponent}Libs)
endforeach()

set(Boost_INCLUDE_DIRS ${BoostSourceDir})
set(Boost_LIBRARY_DIRS ${BoostSourceDir}/stage/lib)
