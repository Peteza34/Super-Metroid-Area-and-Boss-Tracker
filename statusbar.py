import os
import pygame
import image
from constants import *

def initMenuImages(path):
    menuImage = image.singleImage(path)
    return (menuImage, image.brightenImage(menuImage.copy(), CONFIG_BRIGHTEN_AMOUNT))
        
class StatusBar(pygame.Surface):
    def __init__(self, size, position, settingsObj):
        super().__init__(size, flags = pygame.SRCALPHA)
        self.position = position
        self.font = pygame.font.Font(os.path.join(*STATUS_FONT_PATH), STATUS_FONT_SIZE)
        self.backgroundColor = STATUS_BAR_COLOR
        self.menuImage, self.menuHighlightImage = initMenuImages(CONFIG_PATH)
        self.menuRect = self.menuImage.get_rect(center = CONFIG_POSITION)
        self.resetImage, self.resetHighlightImage = initMenuImages(RESET_PATH)
        self.resetRect = self.resetImage.get_rect(center = RESET_POSITION)
        self.lastMessage = ""
        self.messageCenter = (size[0] // 2, size[1] // 2)
        self.messageImage = None
        self.messageRect = None
        self.drawMessage = False
        self.settingsObj = settingsObj

    def update(self, message, mousePos, click):
        trackerState = 1 #TrackerState.DEFAULT
        
        if self.menuRect.collidepoint(mousePos):
            message = "Settings"
            if click[0]:
                trackerState = 2 #TrackerState.SETTINGS
        
        if self.resetRect.collidepoint(mousePos):
            message = "Reset"
            if click[0]:
                trackerState = 3 #TrackerState.RESET
       
        if message:
            self.drawMessage = True
            if message != self.lastMessage:
                self.messageImage = self.font.render(message, False, WHITISH)
                self.messageRect = self.messageImage.get_rect(center = self.messageCenter)
       
        else:
            self.drawMessage = False
        
        self.lastMessage = message
        return trackerState



    def draw(self, mousePos):
        self.fill(self.backgroundColor)
        if self.drawMessage and self.settingsObj.checkOption("Info Bar"):
            self.blit(self.messageImage, self.messageRect)
        
        self.blit(self.menuHighlightImage if self.menuRect.collidepoint(mousePos) else self.menuImage, self.menuRect)
        self.blit(self.resetHighlightImage if self.resetRect.collidepoint(mousePos) else self.resetImage, self.resetRect)