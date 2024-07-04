import os
import pygame
import image
from constants import *

def initResetText(data, font):
    textLines = {}
    for entry in data:
        textLines[entry[0]] = TextLine(entry[0], entry[1], font)
    return textLines

def initExitImages(data): # used for the checkmark and the X
    exitImage = image.singleImage(data)
    return (exitImage, image.brightenImage(exitImage.copy(), CONFIG_BRIGHTEN_AMOUNT))

class TextLine():
    def __init__(self, text, position, font):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], MENU_OPTION_WIDTH, MENU_OPTION_WIDTH)
        self.isActive = True
        self.textImage = font.render(text, False, WHITE)
        self.textPosition = (position[0] + MENU_TEXT_XOFFSET, position[1] + (MENU_OPTION_WIDTH - self.textImage.get_height()) // 2)

class MenuPanel(pygame.Surface):
    def __init__(self, size, position, menuData):
        super().__init__(size, flags = pygame.SRCALPHA)
        self.position = position
        self.rect = self.get_rect(topleft = position)
        self.textLines = initResetText(menuData, pygame.font.Font(os.path.join(*STATUS_FONT_PATH), MENU_TEXT_SIZE))
        self.exitImage, self.exitImageHighlight = initExitImages(EXIT_IMAGE_PATH)
        self.exitRect = self.exitImage.get_rect(topleft = RESET_EXIT_POSITION)
        self.checkImage, self.checkImageHighlight = initExitImages(RESET_CHECK_PATH)
        self.checkRect = self.checkImage.get_rect(topleft = RESET_CHECK_POSITION)
        self.backgroundImage = image.singleImage(RESET_BACKGROUND_PATH)

    def update(self, mousePos, click):
        trackerState = 3 #TrackerState.RESET
        if not self.get_rect().collidepoint(mousePos) and any(click):
            trackerState = 1 #TrackerState.DEFAULT
        elif self.exitRect.collidepoint(mousePos) and click[0]:
            trackerState = 1 #TrackerState.DEFAULT
        elif self.checkRect.collidepoint(mousePos) and click[0]:
            trackerState = 4 #TrackerState.RESETTING
        return trackerState

    def draw(self, mousePos):
        self.fill(BLACK)
        self.blit(self.backgroundImage, ORIGIN)
        
        for textLine in self.textLines.values(): # draw the text
            self.blit(textLine.textImage, textLine.position)
        
        self.blit(self.checkImageHighlight if self.checkRect.collidepoint(mousePos) else self.checkImage, self.checkRect)
        self.blit(self.exitImageHighlight if self.exitRect.collidepoint(mousePos) else self.exitImage, self.exitRect)
