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

Recommand Python 3 (2 is not tested)

Required python library: pygame pyopengl

Required c++ library: libsdl libpng libpython libopengl

Boost will be installed with make script 

```bash
cmake -G "Unix Makefiles"
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




