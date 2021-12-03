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
    pyglet.graphics.draw (4, pyglet.gl.GL_QUADS,
                         ('v2f', [x, y, x + width, y, x + width, y + height, x, y + height]))


#Window Params

WIDTH = 1000
HEIGHT = 800


###############################
##Vector maths

class Vector:
    x = 0
    y = 0
    z = 0

    def  __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector (self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, value):
        return Vector (self.x * value, self.y * value, self.z * value)

    def __str__(self):
        print("X: " + self.x)
        print("Y: " + self.y)
        print("Z: " + self.z)

    def getArray(self):
        return [self.x, self.y, self.z]

def CrossProduct (vector1, vector2):
    crossed_vector = numpy.cross ([vector1.x, vector1.y, vector1.z],[vector2.x, vector2.y, vector2.z])
    return Vector (crossed_vector[0], crossed_vector[1], crossed_vector[2])

def getForwardVector (yaw, pitch):
    forward_vector = Vector (math.sin (math.radians (yaw)) * math.cos (math.radians (pitch)),
                             math.sin (math.radians (pitch)),
                             math.cos (math.radians (yaw)) * math.cos (math.radians (pitch)))
    return forward_vector

def transform_to_player_view (vertex, dx, dy):
    #This is unfinished
    return vertex

import numpy as np

#This has been copied.... no plagiarism. it seems?
# RPY/Euler angles to Rotation Vector
def euler_to_rotVec(yaw, pitch, roll):
    # compute the rotation matrix
    Rmat = euler_to_rotMat(yaw, pitch, roll)

    theta = math.acos(((Rmat[0, 0] + Rmat[1, 1] + Rmat[2, 2]) - 1) / 2)
    sin_theta = math.sin(theta)
    if sin_theta == 0:
        rx, ry, rz = 0.0, 0.0, 0.0
    else:
        multi = 1 / (2 * math.sin(theta))
        rx = multi * (Rmat[2, 1] - Rmat[1, 2]) * theta
        ry = multi * (Rmat[0, 2] - Rmat[2, 0]) * theta
        rz = multi * (Rmat[1, 0] - Rmat[0, 1]) * theta
    return rx, ry, rz

def euler_to_rotMat (yaw, pitch, roll):
    Rz_yaw = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [          0,            0, 1]])
    Ry_pitch = np.array([
        [ np.cos(pitch), 0, np.sin(pitch)],
        [             0, 1,             0],
        [-np.sin(pitch), 0, np.cos(pitch)]])
    Rx_roll = np.array([
        [1,            0,             0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]])
    # R = RzRyRx
    rotMat = np.dot(Rz_yaw, np.dot(Ry_pitch, Rx_roll))
    return rotMat


def getCenterOfVertices (v, num_vertices):
    x = []
    y = []
    z = []
    for index in range (0, int (num_vertices/3)):
        x.append (v.vertices[index * 3])
        y.append (v.vertices[index * 3 + 1])
        z.append (v.vertices[index * 3 + 2])

    center = (max(x)+min(x))/2., (max(y)+min(y))/2., (max(z)+min(z))/2.
    return center

def rotatePoint (pos_vector, rot_vector, center):
    """ An unnecessary amount of fuckery went into sorting this out """
    vX = pos_vector[0] - center[0]
    vY = pos_vector[1] - center[1]
    vZ = pos_vector[2] - center[2]

    rX = math.radians (rot_vector[0])
    rY = math.radians (rot_vector[1])
    rZ = math.radians (rot_vector[2])

    #vX,vY,vZ is the vector coords
    #rx,rY,rZ is the rotation angles in radians
    #Xrotation
    xX = vX
    xY = vY * math.cos (rX) - vZ * math.sin (rX)
    xZ = vY * math.sin (rX) + vZ * math.cos (rX)
    #Yrotation
    yX = xZ * math.sin (rY) + xX * math.cos (rY)
    yY = xY
    yZ = xZ * math.cos (rY) - xX * math.sin (rY)
    #Zrotation
    zX = yX * math.cos (rZ) - yY * math.sin (rZ)
    zY = yX * math.sin (rZ) + yY * math.cos (rZ)
    zZ = yZ

    return (zX + center[0], zY + center[1], zZ + center[2])

def rotatePointRadians (pos_vector, rot_vector, center):
    """ An unnecessary amount of fuckery went into sorting this out """
    vX = pos_vector[0] - center[0]
    vY = pos_vector[1] - center[1]
    vZ = pos_vector[2] - center[2]

    rX =  (rot_vector[0])
    rY =  (rot_vector[1])
    rZ =  (rot_vector[2])

    #vX,vY,vZ is the vector coords
    #rx,rY,rZ is the rotation angles in radians
    #Xrotation
    xX = vX
    xY = vY * math.cos (rX) - vZ * math.sin (rX)
    xZ = vY * math.sin (rX) + vZ * math.cos (rX)
    #Yrotation
    yX = xZ * math.sin (rY) + xX * math.cos (rY)
    yY = xY
    yZ = xZ * math.cos (rY) - xX * math.sin (rY)
    #Zrotation
    zX = yX * math.cos (rZ) - yY * math.sin (rZ)
    zY = yX * math.sin (rZ) + yY * math.cos (rZ)
    zZ = yZ

    return (zX + center[0], zY + center[1], zZ + center[2])

def rotatePointWithOffset (pos_vector, rot_vector, center, rot_offset):
    """ An unnecessary amount of fuckery went into sorting this out """
    vX = pos_vector[0] - center[0]
    vY = pos_vector[1] - center[1]
    vZ = pos_vector[2] - center[2]

    rX = math.radians (rot_vector[0]) + math.radians(rot_offset[0])
    rY = math.radians (rot_vector[1]) + math.radians(rot_offset[1])
    rZ = math.radians (rot_vector[2]) + math.radians(rot_offset[2])

    print("rX:" + str(math.degrees(rX)))
    print("rY:" + str(math.degrees(rY)))
    print("rZ:" + str(math.degrees(rZ)))

    #vX,vY,vZ is the vector coords
    #rx,rY,rZ is the rotation angles in radians
    #Xrotation
    xX = vX
    xY = vY * math.cos (rX) - vZ * math.sin (rX)
    xZ = vY * math.sin (rX) + vZ * math.cos (rX)
    #Yrotation
    yX = xZ * math.sin (rY) + xX * math.cos (rY)
    yY = xY
    yZ = xZ * math.cos (rY) - xX * math.sin (rY)
    #Zrotation
    zX = yX * math.cos (rZ) - yY * math.sin (rZ)
    zY = yX * math.sin (rZ) + yY * math.cos (rZ)
    zZ = yZ

    return (zX + center[0], zY + center[1], zZ + center[2])

###############################



#Object parameters here
GRASS = tex_coords ((1, 0), (0, 1), (0, 0))
SAND = tex_coords ((1, 1), (1, 1), (1, 1))
BRICK = tex_coords ((2, 0), (2, 0), (2, 0))
STONE = tex_coords ((2, 1), (2, 1), (2, 1))

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]
