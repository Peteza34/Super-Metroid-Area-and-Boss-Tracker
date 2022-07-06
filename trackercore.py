import pygame
import areatracker, itemtracker, statusbar, menu, settings
from enum import Enum
from constants import *

def initSettingsObject(data):
    options = {}
    for entry in data:
        options[entry[0]] = True
    return settings.Settings(options)

#Indicates whether the settings menu is open or not
class TrackerState(Enum):
    DEFAULT = 1
    SETTINGS = 2

class TrackerCore(pygame.Surface):
    def __init__(self, size, backgroundImage):    
        super().__init__(size, flags = pygame.SRCALPHA)
        self.settingsObj = initSettingsObject(SETTINGS_DATA)
        self.itemTracker = itemtracker.ItemTracker(ITEM_TRACKER_SIZE, ITEM_TRACKER_POSITION, ITEM_DATA)
        self.areaTracker = areatracker.AreaTracker(AREA_TRACKER_SIZE, AREA_TRACKER_POSITION, NODE_DATA, NODE_COLORS, AREA_MAP_PATH, BASE_NODE_PATH, ARROW_PATH, TRASHCAN_PATH, TRASHCAN_POSITION, BOSS_PATHS, BOSS_DATA, self.settingsObj)
        self.statusBar = statusbar.StatusBar(STATUS_BAR_SIZE, STATUS_BAR_POSITION, self.settingsObj)
        self.settingsMenu = menu.MenuPanel(MENU_SIZE, MENU_POSITION, SETTINGS_DATA, self.settingsObj)
        self.backgroundImage = backgroundImage
        self.trackerState = TrackerState.DEFAULT

        #Start with suit indicators off, because I don't like using it
        self.settingsMenu.options["Suit Indicators"].isActive = self.settingsObj.toggleOption("Suit Indicators")

    def update(self, mousePos, click):
        #update trackers, get mouse hover message, and send it to the statusbar
        message = ""
        if self.trackerState == TrackerState.DEFAULT: 
            message += self.itemTracker.update((mousePos[0] - self.itemTracker.position[0], mousePos[1] - self.itemTracker.position[1]), click)
            message += self.areaTracker.update((mousePos[0] - self.areaTracker.position[0], mousePos[1] - self.areaTracker.position[1]), click)
            self.trackerState = TrackerState(self.statusBar.update(message, (mousePos[0] - self.statusBar.position[0], mousePos[1] - self.statusBar.position[1]), click))
        elif self.trackerState == TrackerState.SETTINGS: #settings menu open
            self.trackerState = TrackerState(self.settingsMenu.update((mousePos[0] - self.settingsMenu.position[0], mousePos[1] - self.settingsMenu.position[1]), click))
            self.statusBar.drawMessage = False

    def draw(self, mousePosition):
        self.fill(BLACK)
        
        if self.settingsObj.checkOption("Background Image"):
            self.blit(self.backgroundImage, ORIGIN)
       
        #draw the trackers
        self.itemTracker.draw((mousePosition[0] - self.itemTracker.position[0], mousePosition[1] - self.itemTracker.position[1]))
        self.areaTracker.draw((mousePosition[0] - self.areaTracker.position[0], mousePosition[1] - self.areaTracker.position[1]))
        self.statusBar.draw((mousePosition[0] - self.statusBar.position[0], mousePosition[1] - self.statusBar.position[1]))
        
        self.blit(self.itemTracker, self.itemTracker.position)
        self.blit(self.areaTracker, self.areaTracker.position)
        self.blit(self.statusBar, self.statusBar.position)

        #Settings menu open
        if self.trackerState == TrackerState.SETTINGS:
            self.settingsMenu.draw((mousePosition[0] - self.settingsMenu.position[0], mousePosition[1] - self.settingsMenu.position[1]))
            self.blit(self.settingsMenu, self.settingsMenu.position)