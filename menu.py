import os
import pygame
import image
from constants import *

def initMenuOptions(data, font):
    menuOptions = {}
    for entry in data:
        menuOptions[entry[0]] = MenuOption(entry[0], entry[1], font)
    return menuOptions

def initMenuImages(data):
    images = {}

    imageActive = image.singleImage(data[0])
    imageActiveHighlight = image.changeColorIgnoreAlpha(imageActive.copy(), WHITISH, WHITE)
    imageInactive = image.singleImage(data[1])
    imageInactiveHighlight = image.changeColorIgnoreAlpha(imageInactive.copy(), WHITISH, WHITE)

    images["active"] = imageActive
    images["activeHighlight"] = imageActiveHighlight
    images["inactive"] = imageInactive
    images["inactiveHighlight"] = imageInactiveHighlight
    
    return images

def initExitImages(data):
    exitImage = image.singleImage(data)
    return (exitImage, image.brightenImage(exitImage.copy(), CONFIG_BRIGHTEN_AMOUNT))

class MenuOption():
    def __init__(self, text, position, font):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], MENU_OPTION_WIDTH, MENU_OPTION_WIDTH)
        self.isActive = True
        self.textImage = font.render(text, False, WHITE)
        self.textPosition = (position[0] + MENU_TEXT_XOFFSET, position[1] + (MENU_OPTION_WIDTH - self.textImage.get_height()) // 2)

class MenuPanel(pygame.Surface):
    def __init__(self, size, position, menuData, settingsObj):
        super().__init__(size, flags = pygame.SRCALPHA)
        self.position = position
        self.rect = self.get_rect(topleft = position)
        self.options = initMenuOptions(menuData, pygame.font.Font(os.path.join(*STATUS_FONT_PATH), MENU_TEXT_SIZE))
        self.settingsObj = settingsObj
        self.exitImage, self.exitImageHighlight = initExitImages(EXIT_IMAGE_PATH)
        self.exitRect = self.exitImage.get_rect(topleft = MENU_EXIT_POSITION)
        self.backgroundImage = image.singleImage(MENU_BACKGROUND_PATH)
        self.images = initMenuImages(MENU_IMAGE_PATHS)

    def update(self, mousePos, click):
        trackerState = 2 #TrackerState.SETTINGS
        if not self.get_rect().collidepoint(mousePos) and any(click):
            trackerState = 1 #TrackerState.DEFAULT
        else:
            for key, val in self.options.items():
                if val.rect.collidepoint(mousePos) and click[0]:
                    val.isActive = self.settingsObj.toggleOption(key)
            if self.exitRect.collidepoint(mousePos) and click[0]:
                trackerState = 1 #TrackerState.DEFAULT
        return trackerState

    def draw(self, mousePos):
        self.fill(BLACK)
        self.blit(self.backgroundImage, ORIGIN)
        
        for option in self.options.values():
            key = "active" if option.isActive else "inactive"
            if option.rect.collidepoint(mousePos):
                key += "Highlight"
            
            self.blit(option.textImage, option.textPosition)
            self.blit(self.images[key], option.position)
        
        self.blit(self.exitImageHighlight if self.exitRect.collidepoint(mousePos) else self.exitImage, self.exitRect)
