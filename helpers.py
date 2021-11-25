import Settings
from Settings import *


# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

# Number of ticks per second
TICKS_PER_SEC = 60

TEXTURE_PATH = 'texture.png'



def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.
        Probably the most shameful way to write this out. There is a way to do
        it algorithmically. Tip: Find a fast way to count binary and then
        substitute digits for operations. Is it necessary? Does it improve the
        way the code is written? I'm not really sure.
    """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]



if sys.version_info[0] >= 3:
    xrange = range

def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)


def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)


########Get Vectors############
def get_sight_vector(self):
    """ Returns the current line of sight vector indicating the direction
    the player is looking.

    """
    x, y = self.rotation
    # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
    # is 1 when looking ahead parallel to the ground and 0 when looking
    # straight up or down.
    m = math.cos(math.radians(y))
    # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
    # looking straight up.
    dy = math.sin(math.radians(y))
    dx = math.cos(math.radians(x - 90)) * m
    dz = math.sin(math.radians(x - 90)) * m
    return (dx, dy, dz)

def get_motion_vector(self):
    """ Returns the player's velocity vector

    Returns
    -------
    vector : tuple of len 3
        Tuple containing the velocity in x, y, and z respectively.

    """
    if any(self.strafe):
        x, y = self.rotation
        strafe = math.degrees(math.atan2(*self.strafe))
        y_angle = math.radians(y)
        x_angle = math.radians(x + strafe)
        if self.flying:
            m = math.cos(y_angle)
            dy = math.sin(y_angle)
            if self.strafe[1]:
                # Moving left or right.
                dy = 0.0
                m = 1
            if self.strafe[0] > 0:
                # Moving backwards.
                dy *= -1
            # When you are flying up or down, you have less left and right
            # motion.
            dx = math.cos(x_angle) * m
            dz = math.sin(x_angle) * m
        else:
            dy = 0.0
            dx = math.cos(x_angle)
            dz = math.sin(x_angle)
    else:
        dy = 0.0
        dx = 0.0
        dz = 0.0
    return (dx, dy, dz)



###############################
##Graphics helper Functions

def draw_rect(x, y, width, height):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
        ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))


#Window Params

WIDTH = 1000
HEIGHT = 800


###############################







#Object parameters here
GRASS = tex_coords((1, 0), (0, 1), (0, 0))
#GRASS = tex_coords((2, 1), (2, 1), (2, 2))
#SAND = tex_coords((1, 1), (1, 1), (1, 1))
#BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

INVENTORY = []
