import pygame
import os
from constants import *

#pathString = image path as list
def singleImage(pathStrings):
    return pygame.image.load(os.path.join(*pathStrings)).convert_alpha()

#Assumes background is same size as image
#Will give it a black background if background = None
def addBackground(image, background = None):
    if not background:
        background = pygame.Surface(image.get_size(), flags = pygame.SRCALPHA)
        background.fill((0, 0, 0, 255))
    background.blit(image, (0, 0))
    return background

#Checks each pixel of the image and if it matches oldColor, replace it with newColor
def changeColor(image, oldColor, newColor):
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            if image.get_at((x, y)) == oldColor:
                image.set_at((x, y), newColor) 
    return image

#Checks each pixel of the image and if the rbg value matches oldColor(regardless of alpha value), replace it with newColor
def changeColorIgnoreAlpha(image, oldColor, newColor):
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            if image.get_at((x, y))[:-1] == oldColor[:-1]:
                image.set_at((x, y), newColor) 
    return image

#Dims image by adding some amount of black to it
#dimPercent = int 1-100, 100 will make it completely black
def dimImage(image, dimPercent):
    mask = pygame.Surface(image.get_size()).convert_alpha()
    mask.fill((0, 0, 0, (dimPercent * 255 // 100)))

    #check for transparent pixels and exclude them
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            if tuple(image.get_at((x, y)))[-1] == 0:
                mask.set_at((x, y), TRANSPARENT)
    
    image.blit(mask, ORIGIN)
    return image

#increases the rgb value of each non-transparent pixel by a set amount
def brightenImage(image, brightenAmount):
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            color = tuple(image.get_at((x, y)))
            if color[-1] > 0:
                image.set_at((x, y), [min(255, val + brightenAmount) for val in color])
    return image