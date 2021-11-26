import helpers
from helpers import *

""" We're using lists to store items, and we need to construct a wrapper for the inventory
    that allows both for access into it as well as encapsulation of the draw functions.
"""
class Inventory():
    def __init__ (self, batch, group):
        self.item_list = []
        self.item_count = []
        self.InventoryWidth = WIDTH * 0.7
        self.InventoryHeight = HEIGHT * 0.1
        self.InventoryXPos = (WIDTH - self.InventoryWidth ) / 2.0
        self.InventoryYPos = 40
        self.index = 0
        self.batch = batch
        self.group = group

        self.v = self.draw_3D_inventory_block (0, 10, 0, GRASS)


    def draw_3D_inventory_block (self, x, y, z, texture):
        vertex_data = cube_vertices (x, y, z, 1)
        self.batch.invalidate()
        glOrtho(0, width, 0, height, -1, 1)
        v = self.batch.add (24, GL_QUADS, self.group, ('v3f/static', vertex_data), ('t2f/static', texture))
        return v

    def draw (self):
        return
#        glColor3f (1,0,0)
#        draw_rect (self.InventoryXPos, self.InventoryYPos, self.InventoryWidth, self.InventoryHeight)

    def drawIndividualItem (self, index, group, player_pos, camera_rot):
        """ I think that inventory items should be drawn either as 2D sprites or 3D icons. I'm not
            sure yet. However I am sure that I don't like the sprite sheet method of loading
            sprites. However we may not have another choice due to speed constraints, I guess?

            No. I have decided on 2D sprites that we pre-render.
        """
#        glColor3f (0,1,0)
#        tex.target = self.item_list[index]
#        glEnable (GL_TEXTURE_2D)
#        glBindTexture (GL_TEXTURE_2D, tex.id)
        x = self.InventoryXPos + 37 + self.InventoryWidth / 9 * index
        y = self.InventoryYPos

        forward_x = math.sin (math.radians(camera_rot[0])) * math.cos (math.radians(camera_rot[1]))
        forward_y = math.sin (math.radians(camera_rot[1]))
        forward_z = math.cos (math.radians(camera_rot[0])) * math.cos (math.radians(camera_rot[1]))

        transformed_x = player_pos[0] + forward_x * 10
        transformed_y = player_pos[1] + forward_y * 10
        transformed_z = player_pos[2] - forward_z * 10

        self.v.vertices = cube_vertices (transformed_x, transformed_y, transformed_z, 1)
        num_vertices = self.v.get_size() * 3
        center_pos = getCenterOfVertices (self.v, num_vertices)

        for index in range (0, num_vertices, 3):
            xvert = index
            yvert = index + 1
            zvert = index + 2

            camera_rot_z = numpy.arctan(math.sqrt(camera_rot[1] * camera_rot[1] + camera_rot[0] * camera_rot[0]))
            camera_rot_z = 0

            rotated_vector = rotatePoint ((self.v.vertices[xvert],
                                           self.v.vertices[yvert],
                                           self.v.vertices[zvert]),
                #                           (0, 10, 0),
                                    #        (0, 0, -camera_rot[1]), #this constrains vertically at 4 points on the curve
                                          (0, -camera_rot[0], 0), # This constrains horizontally
                                           center_pos)

    #        print(camera_rot)

            self.v.vertices[xvert] = rotated_vector[0]
            self.v.vertices[yvert] = rotated_vector[1]
            self.v.vertices[zvert] = rotated_vector[2]

    #        print(a)

#        batch.draw()

#        draw_rect (self.InventoryXPos + 37+self.InventoryWidth/9*index, self.InventoryYPos, self.InventoryWidth / 10.0, self.InventoryHeight)

    def drawItems (self, batch, group, player_pos, camera_rot):
        """ maybe I should wrap batch and group as another object"""
        for index in range (0, len (self.item_list)):
            self.drawIndividualItem (index, group, player_pos, camera_rot)
        return

    def getCurrentlyIndexedItem (self):
        if (len (self.item_list) <= self.index):
            return None
        else:
            return (self.item_list [self.index])

    def addItem (self, item_name):
        for i in range (0, len (self.item_list)):
            if (self.item_list [i] == item_name):
                self.item_count [i] = self.item_count [i] + 1
                return
        """ if the code doesn't break, we then add the item and its count to their respective lists """
        self.item_list.append (item_name)
        self.item_count.append (1)

    def removeItem (self, item_name):
        for i in range (0, len (self.item_list)):
            if (self.item_list[i] == item_name):
                self.item_count[i] = self.item_count[i] - 1
                if self.item_count[i] <= 0:
                    del self.item_list[i]
                    del self.item_count[i]

    def setIndex (self, i):
        self.index = i

    def getSize (self):
        return len (self.item_list)
