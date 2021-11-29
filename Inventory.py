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

        self.pos_z = 0

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

            3D is the way to gooo
        """
#        glColor3f (0,1,0)
#        tex.target = self.item_list[index]
#        glEnable (GL_TEXTURE_2D)
#        glBindTexture (GL_TEXTURE_2D, tex.id)
        x = self.InventoryXPos + 37 + self.InventoryWidth / 9 * index
        y = self.InventoryYPos

        yaw = camera_rot[0]
        pitch = camera_rot[1]

        forward_vector = getForwardVector (yaw, pitch )
        transform_vector = Vector (0,1,0)
        player_vector = Vector (player_pos[0], player_pos[1], player_pos[2])
        right_vector = CrossProduct (forward_vector, transform_vector)
        up_vector = CrossProduct (right_vector, forward_vector)

        transformed_x = player_pos[0] + forward_vector.x * 10
        transformed_y = player_pos[1] + forward_vector.y * 10
        transformed_z = player_pos[2] - forward_vector.z * 10

        self.v.vertices = cube_vertices (transformed_x, transformed_y, transformed_z, 1)
        num_vertices = self.v.get_size() * 3
        center_pos = getCenterOfVertices (self.v, num_vertices)


        self.pos_z = self.pos_z + 1

        for index in range (0, num_vertices, 3):
            xvert = index
            yvert = index + 1
            zvert = index + 2


            #rotates cube to face player
            rotated_vector = rotatePoint ((self.v.vertices[xvert],
                                           self.v.vertices[yvert],
                                           self.v.vertices[zvert]),
                                           (pitch, -yaw, 0),
                                           center_pos)

            self.v.vertices[xvert] = rotated_vector[0]
            self.v.vertices[yvert] = rotated_vector[1]
            self.v.vertices[zvert] = rotated_vector[2]


#            self.v.vertices[xvert] = self.v.vertices[xvert] - up_vector.x * 5
#            self.v.vertices[yvert] = self.v.vertices[yvert] - up_vector.y * 5
#            self.v.vertices[zvert] = self.v.vertices[zvert] + up_vector.z * 5

            #Opposite signage because left
#            self.v.vertices[xvert] = self.v.vertices[xvert] + right_vector.x * 5
#            self.v.vertices[yvert] = self.v.vertices[yvert] + right_vector.y * 5
#            self.v.vertices[zvert] = self.v.vertices[zvert] - right_vector.z * 5


            positioning_vector = right_vector * 10

            print("Pitch: " + str(pitch))
            print("Yaw:" + str(yaw))

            #rotates cube with player as center as a pseudo positioning
            #i need to calculate new pitch and yaw from line of sight, pitch and yaw

            #yaw and pitch only provide rotational information in 360 degrees. I need to make sure
            #that the rotation from x axis is always kept in mind, and then add rotation based on that



            rotated_vector = rotatePoint ((self.v.vertices[xvert],
                                           self.v.vertices[yvert],
                                           self.v.vertices[zvert]),
                                          (20, 0, 0), #this shit is in the x and y and z axes. I need to SHIFT THE AXES SUCH THAT THE FORWARD VECTOR IS THE X AXES
                                           player_pos)

    #        print("Rotated_x" + str(rotated_vector[0]))
    #        print("Rotated_y" + str(rotated_vector[1]))
    #        print("Rotated_z" + str(rotated_vector[2]))

            self.v.vertices[xvert] = rotated_vector[0]
            self.v.vertices[yvert] = rotated_vector[1]
            self.v.vertices[zvert] = rotated_vector[2]

            pivotPoint = [0,0,0]
            pivotPoint[0] = player_pos[0] + right_vector.x * 5
            pivotPoint[1] = player_pos[1] + right_vector.y * 5
            pivotPoint[2] = player_pos[2] - right_vector.z * 5



        """ now we have to move the cube into its respective slot """



#            self.v.vertices[xvert] = transform_to_player_view (self.v.vertices[xvert], -30, -30)

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
