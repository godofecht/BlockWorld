import helpers
from helpers import *

""" We're using lists to store items, and we need to construct a wrapper for the inventory
    that allows both for access into it as well as encapsulation of the draw functions.
"""
class Inventory():
    def __init__ (self, batch, group):
        self.item_list = [GRASS,STONE]
        self.item_count = [1,1]
        self.InventoryWidth = WIDTH * 0.7
        self.InventoryHeight = HEIGHT * 0.1
        self.InventoryXPos = (WIDTH - self.InventoryWidth ) / 2.0
        self.InventoryYPos = 40
        self.index = 0
        self.batch = pyglet.graphics.Batch()
        self.group = group
        self.item_v = []
        self.item_v.append (self.draw_3D_inventory_block (0, 1, 0, GRASS))
        self.item_v.append (self.draw_3D_inventory_block (1, 1, 0, STONE))


    def draw_3D_inventory_block (self, x, y, z, texture):
        vertex_data = cube_vertices (x, y, z, 1)
        self.batch.invalidate()
        glOrtho(0, width, 0, height, -1, 1)
        v = self.batch.add (24, GL_QUADS, self.group, ('v3f/static', vertex_data), ('t2f/static', texture))
        return v

    def draw (self):
        self.batch.draw()
        return
#        glColor3f (1,0,0)
#        draw_rect (self.InventoryXPos, self.InventoryYPos, self.InventoryWidth, self.InventoryHeight)

    def drawIndividualItem (self, index, group, player_pos, camera_rot, item_vertices):
        """ I think that inventory items should be drawn either as 2D sprites or 3D icons. I'm not
            sure yet. However I am sure that I don't like the sprite sheet method of loading
            sprites. However we may not have another choice due to speed constraints, I guess?

            3D is the way to gooo
        """

        x = self.InventoryXPos + 37 + self.InventoryWidth / 9 * index
        y = self.InventoryYPos

        yaw = camera_rot[0]
        pitch = camera_rot[1]

        rot_offsetx = index * 16 - 32
        rot_offsety = -18

        forward_vector = getForwardVector (rot_offsetx, rot_offsety)
        transform_vector = Vector (0, 1, 0)
        player_vector = Vector (player_pos[0], player_pos[1], player_pos[2])
        right_vector = CrossProduct (forward_vector, transform_vector)
        up_vector = CrossProduct (right_vector, forward_vector)

        offset_forward_vector = getForwardVector (yaw, pitch)

        if index == self.index: #maybe change self.index to self.currently_selected_index or something
            projection_distance_factor = 8
        else:
            projection_distance_factor = 10

        transformed_x = player_pos[0] + forward_vector.x * projection_distance_factor
        transformed_y = player_pos[1] + forward_vector.y * projection_distance_factor
        transformed_z = player_pos[2] - forward_vector.z * projection_distance_factor

        item_vertices.vertices = cube_vertices (transformed_x, transformed_y, transformed_z, 1)
        num_vertices = item_vertices.get_size() * 3
        center_pos = getCenterOfVertices (item_vertices, num_vertices)


        for index in range (0, num_vertices, 3):
            xvert = index
            yvert = index + 1
            zvert = index + 2

            #rotates cube by offset
            rotated_vector = rotatePoint ((item_vertices.vertices[xvert],
                                           item_vertices.vertices[yvert],
                                           item_vertices.vertices[zvert]),
                                           (rot_offsety, -rot_offsetx, 0),
                                           center_pos)

            item_vertices.vertices[xvert] = rotated_vector[0]
            item_vertices.vertices[yvert] = rotated_vector[1]
            item_vertices.vertices[zvert] = rotated_vector[2]

            #rotates cube to face player
            rotated_vector = rotatePoint ((item_vertices.vertices[xvert],
                                           item_vertices.vertices[yvert],
                                           item_vertices.vertices[zvert]),
                                           (pitch, -yaw, 0),
                                           player_pos)

            item_vertices.vertices[xvert] = rotated_vector[0]
            item_vertices.vertices[yvert] = rotated_vector[1]
            item_vertices.vertices[zvert] = rotated_vector[2]


#            self.v.vertices[xvert] = self.v.vertices[xvert] - up_vector.x * 5
#            self.v.vertices[yvert] = self.v.vertices[yvert] - up_vector.y * 5
#            self.v.vertices[zvert] = self.v.vertices[zvert] + up_vector.z * 5

            #Opposite signage because left
#            self.v.vertices[xvert] = self.v.vertices[xvert] + right_vector.x * 5
#            self.v.vertices[yvert] = self.v.vertices[yvert] + right_vector.y * 5
#            self.v.vertices[zvert] = self.v.vertices[zvert] - right_vector.z * 5


            positioning_vector = right_vector * 10

#            print("Pitch: " + str(pitch))
#            print("Yaw:" + str(yaw))

            #rotates cube with player as center as a pseudo positioning
            #i need to calculate new pitch and yaw from line of sight, pitch and yaw

            #yaw and pitch only provide rotational information in 360 degrees. I need to make sure
            #that the rotation from x axis is always kept in mind, and then add rotation based on that

            xcomp = math.cos (math.radians(pitch)) * math.cos(math.radians(-yaw)) * 20
            ycomp = math.sin (math.radians(pitch)) * 20
            zcomp = math.sin (math.radians(-yaw)) * math.cos(math.radians(pitch)) * 20





    #        print("xcomp: " + str(xcomp))
    #        print("ycomp: " + str(ycomp))
    #        print("zcomp: " + str(zcomp))

    #        print("Rotated_x" + str(rotated_vector[0]))
    #        print("Rotated_y" + str(rotated_vector[1]))
    #        print("Rotated_z" + str(rotated_vector[2]))


    #        print("right_vector_x: " + str(right_vector.z))

    #        self.v.vertices[xvert] = self.v.vertices[xvert] + right_vector.x * 5
    #        self.v.vertices[yvert] = self.v.vertices[yvert] + right_vector.y * 5
    #        self.v.vertices[zvert] = self.v.vertices[zvert] - right_vector.z * 5

#        item_vertices.draw(pyglet.gl.GL_POINTS)
    #    """ now we have to move the cube into its respective slot """



#            self.v.vertices[xvert] = transform_to_player_view (self.v.vertices[xvert], -30, -30)

    #        print(a)

#        batch.draw()

#        draw_rect (self.InventoryXPos + 37+self.InventoryWidth/9*index, self.InventoryYPos, self.InventoryWidth / 10.0, self.InventoryHeight)

    def drawItems (self, batch, group, player_pos, camera_rot):
        """ maybe I should wrap batch and group as another object"""
        for index in range (0, len (self.item_list)):
            self.drawIndividualItem (index, group, player_pos, camera_rot, self.item_v[index])
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
        """ if the code doesn't return, we then add the item and its count to their respective lists """
        self.item_list.append (item_name)
        self.item_count.append (1)
        self.item_v.append(self.draw_3D_inventory_block (len (self.item_count), 1, 0, item_name))

    def removeItem (self, item_name):
        for i in range (0, len (self.item_list)):
            if (self.item_list[i] == item_name):
                self.item_count[i] = self.item_count[i] - 1
                if self.item_count[i] <= 0:
                    del self.item_list[i]
                    del self.item_count[i]
                    del self.item_v[i]
                    return

    def setIndex (self, i):
        self.index = i

    def getSize (self):
        return len (self.item_list)
