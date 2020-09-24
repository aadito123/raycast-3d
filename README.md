# raycast-3d
using raycasting to create a pseudo-3d projection

raycast.py is the 2D overview of the particle.
WASD control movement and the mouse controls where the particle is looking.
The movement controls are relative to where the particles is looking.
The white lines are drawn with openGL to help the framerate.
Field of view is 90 degrees. 
Lines 45-54 set the walls. Change the first 4 integers to change the walls. format: x1, y1, x2, y2

raycast-projection.py is the pseudo 3D implementation.
Everything was drawn with openGL to help with the framerate however, the framerate still chugs at around ~20fps. Might be because of:
 - Python being slow (C++ would be better)
 - Pyglet might be too slow at rendering
 - Inefficiencies in the code (create_rays function)
Same controls as in ray-cast.py. The map is also the same.
Some lighitng techniques are required to help the perception of corners.
Lines 45-54 set the walls. Change the first 4 integers to change the walls. format: x1, y1, x2, y2

Doom (1993) had a slightly easier time making the raycasting calculations because the maps were created using 2D arrays, with different values indicating boundary types.
See this video to understand how that was implemented: https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage
My implementation has me using a Ray class and a Boundary class (denoted as the line object in Pyglet), then uses some linear algebra to calculate the intersection 
points of the ray and the boundaries.
