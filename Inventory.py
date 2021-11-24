import helpers
from helpers import *
from Model import Model

class Inventory():
    def __init__ (self):
        self.item_list = [2] * 8
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
        for index in range (len (self.item_list)):
            self.drawIndividualItem (index)

    def getCurrentlyIndexedItem (self):
        return (self.item_list [self.index])
