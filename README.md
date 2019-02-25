# PythonCraft
Python Minecraft Clone

Demo
====
![](https://raw.githubusercontent.com/zzh8829/PythonCraft/master/demo1.png)
![](https://raw.githubusercontent.com/zzh8829/PythonCraft/master/demo2.png)

Features
========
Reading original minecraft map file

Putting/removing blocks

Build
========

Recommand Python 3 on Mac OS (Windows or Python 2 are not supported)

Required python library: pygame pyopengl

Required c++ library: libsdl libpng libpython libopengl

Installing Library on Mac
```bash
brew install libpng
brew install python3
brew install sdl sdl_ttf sdl_image sdl_mixer
pip install hg+http://bitbucket.org/pygame/pygame
pip install pyopengl
```

Boost will be installed with make script 

Build Project
```bash
cmake -G "Unix Makefiles" .
make
python PythonCraft.py
```

Architecture
============
Python:

*  Create windows with PyGame

*  Create OpenGL context with PyOpenGL

*  Render environment and GUI



C++:

 * Read map data
  
 * Render map




