# ch_bl_geodesics
Geodesics algorithm for Blender using ChenHan algorithm

This Blender-Addon is based on the geodesic algorithm of Shiqing Xin and based on his paper

Xin SQ, Wang GJ. Improving Chen and Han's algorithm on the discrete geodesic problem. ACM Transactions on Graphics (TOG). 2009 Aug 1;28(4):104.

The idea is to use this geodesic algorithm for segmentation of meshes. This feature is not available yet. But an user can see the path between two points on a mesh with consecutive clicks. 

Remember, this plugin is very slow as of now. The python code is just a mere re-implementation of C++ code using replacement packages of python.

Suggestions are welcome. I am not an experienced python programmer yet, so any help will be useful.

Please refer to the wiki section for Install and usage. In case you downloaded this zip, you should find a folder named docs

IMPORTANT UPDATE
----------------

Once you download or clone the repository its named as ch_bl_geodesics. Rename it to chenhan_pp before adding it as an addon to blender. This causes issues in enabling the plugin. After doing this you should be able to resolve this error
