from helpers import *

def GenerateFlatland(self,n,s,y):
  for x in xrange(-n, n + 1, s):
     for z in xrange(-n, n + 1, s):
         # create a layer stone an grass everywhere.
         self.add_block((x, y - 2, z), GRASS, immediate=False)
         self.add_block((x, y - 3, z), STONE, immediate=False)
         if x in (-n, n) or z in (-n, n):
             # create outer walls.
             for dy in xrange(-2, 3):
                 self.add_block((x, y + dy, z), STONE, immediate=False)

def GenerateHills(self,n):
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
