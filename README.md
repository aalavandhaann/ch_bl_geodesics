# chenhan_pp
Geodesics algorithm for Blender using ChenHan algorithm

This Blender-Addon is based on the geodesic algorithm of Shiqing Xin and based on his paper

Xin SQ, Wang GJ. Improving Chen and Han's algorithm on the discrete geodesic problem. ACM Transactions on Graphics (TOG). 2009 Aug 1;28(4):104.

The idea is to use this geodesic algorithm for segmentation of meshes. This feature is not available yet. But an user can see the path between two points on a mesh with consecutive clicks. 

Remember, this plugin is very slow as of now. The python code is just a mere re-implementation of C++ code using replacement packages of python. In case you have time for an adventure then look into this [repository](https://github.com/aalavandhaann/chenhan_cython) converts the implemented algorithm using C++ to python directly. This way native C++ data-types are used, no loss in conversion of numerics every time a call is made, native pairs, maps, lists etc., I checked it myself and timing differences are almost 210x faster than the pure python implementation supplied in this repository. 

Suggestions are welcome and any contributions will be useful.

Please refer to the wiki section for Install and usage. In case you downloaded this zip, you should find a folder named docs

IMPORTANT UPDATE
----------------

Once you download or clone the repository its named as ch_bl_geodesics. Copy the folder named **chenhan_pp** to the blender addons folder for the plugin to work. Otherwise there would be issues in enabling the plugin. After doing this you should be able to resolve this error
