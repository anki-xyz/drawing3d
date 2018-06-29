# drawing3d

This repo offers 3D drawing features for numpy 3D __volume__ stacks (e.g. confocal stacks).
Functions act in-place.

Easy usage, drawing a sphere in a confocal stack with xy resolution = .25 µm and z steps = 1 µm:
```python 
from drawing3d import sphere

stack = np.zeros((50, 100, 100)) # z, x, y
d = 4 # µm
xyz_spacings = [.25, .25, 1] # µm 
x, y, z = 40, 40, 32
sphere(stack, [x,y,z], d, xyz_spacings)
```
