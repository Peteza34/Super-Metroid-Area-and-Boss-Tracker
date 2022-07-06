import pygame
import image
from constants import *

def initItemButtons(data):
    buttons = {}
    images = {}
    for entry in data:
        key = entry[0]

        #find coordinates using grid position
        pos = (entry[1][0] * (ITEM_WIDTH + ITEM_SPACING) + ITEM_SPACING, entry[1][1] * (ITEM_WIDTH + ITEM_SPACING) + ITEM_SPACING)
        buttons[key] = ItemButton(key, pos)

        itemImage = image.dimImage(image.singleImage(entry[2]), ITEM_DIM_PERCENT)
        itemImageInactive = image.dimImage(image.singleImage(entry[2]), ITEM_DIM_PERCENT_INACTIVE)
        
        images[key] = itemImage
        images[key + "Inactive"] = itemImageInactive

        #mouse hover images
        images[key + "Highlight"] = image.brightenImage(itemImage.copy(), ITEM_BRIGHTEN_AMOUNT)
        images[key + "InactiveHighlight"] = image.brightenImage(itemImageInactive.copy(), ITEM_BRIGHTEN_AMOUNT_INACTIVE)       

    return (buttons, images)

class ItemButton:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], ITEM_WIDTH, ITEM_WIDTH)
        self.isActive = False
    
    def __str__(self):
        return self.name

#Handles the logic and presentation of the item tracker
#It is a Pygame Surface, so essentially a drawing canvas
class ItemTracker(pygame.Surface):
    def __init__(self, size, position, itemData):
        super().__init__(size, flags = pygame.SRCALPHA)
        self.position = position 
        self.buttons, self.images = initItemButtons(itemData)

    #update the tracker, returns hover message for statusbar
    def update(self, mousePos, click):
        status = ""
        for item in self.buttons.values():
            if item.rect.collidepoint(mousePos):
                status = str(item)
                if any(click):
                    item.isActive = not item.isActive
        return status

    #Clears the canvas, determines which image to draw for each item, and draws it
    def draw(self, mousePosition):
        self.fill(TRANSPARENT)
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