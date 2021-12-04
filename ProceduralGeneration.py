from helpers import *
#import matplotlib.pyplot as plt

def GenerateFlatland (self, n, s, y):
  for x in xrange(-n, n + 1, s):
     for z in xrange(-n, n + 1, s):
         # create a layer stone an grass everywhere.
         self.add_block((x, y - 2, z), GRASS, immediate=False)
         self.add_block((x, y - 3, z), STONE, immediate=False)
         if x in (-n, n) or z in (-n, n):
             # create outer walls.
             for dy in xrange(-2, 3):
                 self.add_block((x, y + dy, z), STONE, immediate=False)

def GenerateHills (self, n):
        o = n - 10
        for _ in xrange(120):
            a = random.randint(-o, o)  # x position of the hill
            b = random.randint(-o, o)  # z position of the hill
            c = -1  # base of the hill
            h = random.randint(1, 6)  # height of the hill
            s = random.randint(4, 8)  # 2 * s is the side length of the hill
            d = 1  # how quickly to taper off the hills
#            t = random.choice([GRASS, SAND, BRICK])
            t = GRASS
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                s -= d  # decrement side lenth so hills taper off

def GenerateFlatLandBlockList (self, n, s):
    blockList = []
    for x in xrange(-n, n + 1, s):
        for z in xrange(-n, n + 1, s):
            blockList.append (GRASS)
    return blockList

def GenerateLandFromBlockList (self, noise, n, s, y):
    biomeBlockTypeList = GenerateBiomeNoise (self, n, s, y)
    for x in xrange(-n, n + 1, s):
        for z in xrange(-n, n + 1, s):
    #            self.add_block((x, noise[x, z] - 3, z), GRASS, immediate=False)
                for block_height in xrange(-10, int (noise[x, z]) - 3, s):
                    self.add_block((x, block_height, z), biomeBlockTypeList[x * 2 * n + z], immediate=False)


def GeneratePerlinNoise (self, n, s, y):
    blockList = []
    lin = np.linspace (0, 4, n*2, endpoint=False)
    x, z = np.meshgrid (lin,lin) # FIX3: I thought I had to invert x and y here but it was a mistake
    current_time = time.time()
    r = int (random.random () * 1000)
    noise = perlin(x, z, r)
    for x in xrange(-n, n + 1, s):
        for z in xrange(-n, n + 1, s):
            noise[x, z] = - math.floor (noise[x,z] * 4.5)

            for y in xrange(-y, y + 1, s):
                if (noise[x, z] == y):
                    blockList.append (GRASS)

#            print(noise[x, z])
#            self.add_block ((x, noise[x,z] - 2.0, z), GRASS, immediate = False)
#    print(len(blockList))
    return noise

def GenerateBiomeNoise (self, n, s, y):
    blockTypeList = []
    for i in range(0, n*2):
        for j in range(0, n*2):
            blockTypeList.append (GRASS)
    lin = np.linspace (0, 2, n*2, endpoint=False)
    x, z = np.meshgrid (lin,lin) # FIX3: I thought I had to invert x and y here but it was a mistake
    current_time = time.time()
    r = int (random.random () * 1000)
    noise = perlin (x, z, r)
    for x in xrange (-n, n + 1, s):
        for z in xrange (-n, n + 1, s):
            noise[x, z] = - math.floor (noise[x,z] * 4.5)

            if (noise[x, z] > 0):
                blockTypeList[int(x * n * 2 + z)] = GRASS
            else:
                blockTypeList[int(x * n * 2 + z)] = SAND

#            print  (noise[x, z])
#            self.add_block ((x, noise[x,z] - 2.0, z), GRASS, immediate = False)
    return blockTypeList
