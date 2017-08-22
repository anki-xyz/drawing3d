import numpy as np
from numba import jit
from skimage.draw import circle


@jit
def line(s, p0, p1, color=1):
    '''
    Draw a line in 3D space
    :param s: the numpy 3D stack
    :param p0: x, y, z tuple
    :param p1: x, y, z tuple
    :param color: integer, e.g. 255 for np.uint8 stack
    :return: Nothing
    '''
    assert len(p0) == len(p1), "points should have same depth"

    if len(s.shape) == 2:
        s = s[None]
        p0 = p0[0], p0[1], 0
        p1 = p1[0], p1[1], 0

    assert len(s.shape) == 3, "stack s should be 2D or 3D"

    x0, y0, z0 = p0
    x1, y1, z1 = p1
    x, y, z = p0

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    dz = abs(z1 - z0)

    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    sz = -1 if z0 > z1 else 1

    derr = max([dx, dy, dz])

    errx = derr / 2
    erry = derr / 2
    errz = derr / 2

    for i in range(derr):
        s[z, x, y] = color

        errx -= dx

        if errx < 0:
            x += sx
            errx += derr

        erry -= dy

        if erry < 0:
            y += sy
            erry += derr

        errz -= dz

        if errz < 0:
            z += sz
            errz += derr


def sphere(s, p0, d, spacing=[1, 1, 1], color=255, debug=False):
    '''
    Draw a 3D sphere with given diameter d at point p0 in given color.
    :param s: numpy 3D stack
    :param p0: x, y, z tuple
    :param d: diameter in 1 spacing unit
    :param spacing: x, y, z spacing; x and y spacing must be equal
    :param color: draw color, e.g. 255 for np.uint8 stack
    :param debug: if True prints plane related information
    :return: Nothing
    '''

    assert spacing[0] == spacing[1], "x and y spacing must be the same!"

    # Convert to pixels
    d_xy = d / spacing[0]
    r = d_xy / 2

    # Initialize center
    x, y, z = p0

    # Iterate over planes where the sphere is visible
    for plane in range(z - int(d / spacing[2] / 2), z + int(d / spacing[2] / 2) + 1):
        radius = np.sqrt((d / 2) ** 2 - ((plane - z) * spacing[2]) ** 2) / spacing[0]

        if debug:
            print(plane, (plane - z) * spacing[2], "µm to center")
            print(radius * spacing[0], "µm, ", np.round(radius, 3), "px\n")

        # If sphere is to be drawn
        if radius > 0:
            # Draw a circle on a diameter x diameter grid w/ given radius
            rr, cc = circle(d_xy, d_xy, radius)

            # Go to plane in stack and move circle to right position, acts in-place
            s[plane, (rr + x - d_xy).astype(int), (cc + y - d_xy).astype(int)] = color
