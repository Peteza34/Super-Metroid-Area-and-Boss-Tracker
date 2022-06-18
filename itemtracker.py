import pygame
import image
from constants import *

#data = (name, grid position(x, y), image path)
def initItemButtons(data):
    buttons = {}
    images = {}
    for entry in data:
        key = entry[0]

        #find coordinates using grid position
        pos = (entry[1][0] * (ITEM_WIDTH + ITEM_SPACING) + ITEM_SPACING, entry[1][1] * (ITEM_WIDTH + ITEM_SPACING) + ITEM_SPACING)
        buttons[key] = ItemButton(key, pos)

        #default image is very slightly dim, inactive image is substantially more dim
        itemImage = image.dimImage(image.singleImage(entry[2]), ITEM_DIM_PERCENT)
        itemImageInactive = image.dimImage(image.singleImage(entry[2]), ITEM_DIM_PERCENT_INACTIVE)
        
        images[key] = itemImage
        images[key + "Inactive"] = itemImageInactive

        #Slighlty brighter versions of each image used for mouse-hover
        images[key + "Highlight"] = image.brightenImage(itemImage.copy(), ITEM_BRIGHTEN_AMOUNT)
        images[key + "InactiveHighlight"] = image.brightenImage(itemImageInactive.copy(), ITEM_BRIGHTEN_AMOUNT_INACTIVE)       

    return (buttons, images)

#Represents each item on the item tracker
class ItemButton:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], ITEM_WIDTH, ITEM_WIDTH)
        self.isActive = False

#Handles the logic and presentation of the item tracker
#It is a Pygame Surface, so essentially a drawing canvas
class ItemTracker(pygame.Surface):
    def __init__(self, size, position, itemData):
        super().__init__(size, flags = pygame.SRCALPHA)
        self.position = position 
        self.buttons, self.images = initItemButtons(itemData)

    #Any mouse click will toggle the item
    def handleClick(self, mousePosition):
        for val in self.buttons.values():
            if val.rect.collidepoint(mousePosition):
                val.isActive = not val.isActive

    #Clears the canvas, determines which image to draw for each item, and draws it
    def draw(self, mousePosition):
        self.fill(BLACK)
        for key, val in self.buttons.items():
            k = key
            if not val.isActive:
                k += "Inactive"
            if val.rect.collidepoint(mousePosition):
                k += "Highlight"
            self.blit(self.images[k], val.position)

    #Resets item tracker to inital state
    #Not used yet
    def resetTracker(self):
        for button in self.buttons.values():
            button.isActive = False