import helpers
from helpers import *

""" We're using lists to store items, and we need to construct a wrapper for the inventory
    that allows both for access into it as well as encapsulation of the draw functions.
"""
class Inventory():
    def __init__ (self):
        self.item_list = [GRASS]
        self.item_count = [1]
        self.InventoryWidth = WIDTH * 0.7
        self.InventoryHeight = HEIGHT * 0.1
        self.InventoryXPos = (WIDTH - self.InventoryWidth )/2.0
        self.InventoryYPos = 40
        self.index = 0

    def draw (self):
        glColor3f (1,0,0)
        draw_rect (self.InventoryXPos,self.InventoryYPos,self.InventoryWidth,self.InventoryHeight)

    def drawIndividualItem(self,index):
        glColor3f (0,1,0)
        draw_rect (self.InventoryXPos + 37+self.InventoryWidth/9*index,self.InventoryYPos,self.InventoryWidth/10,self.InventoryHeight*0.1)

    def drawItems (self):
#        for index in range (len (self.item_list)):
#            self.drawIndividualItem (index)
        return

    def getCurrentlyIndexedItem (self):
        if (len (self.item_list) <= self.index):
            return None
        else:
            return (self.item_list [self.index])

    def addItem (self, item_name):
        print (item_name)
        for i in range (0, len (self.item_list)):
            if (self.item_list [i] == item_name):
                self.item_count [i] = self.item_count [i] + 1
                return
        """ if the code doesn't break, we then add the item and its count to their respective lists """
        self.item_list.append (item_name)
        self.item_count.append (1)
        print ("failed")

    def removeItem (self, item_name):
        for i in range (0, len (self.item_list)):
            if (self.item_list[i] == item_name):
                self.item_count[i] = self.item_count[i] - 1
                if self.item_count <= 0:
                    del self.item_list[i]
                    del self.item_count[i]

    def setIndex (self, i):
        self.index = i

    def getSize (self):
        return len (self.item_list)
