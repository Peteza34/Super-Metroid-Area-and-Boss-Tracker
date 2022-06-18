'''
This is an area and boss tracker that is meant to be used for area randomizer modes
of the Super Metroid VARIA Randomizer. It is simpler than the one on the VARIA website, 
but is designed to be compact so you can place it alongside a windowed emulator on the
same monitor. I won't be adding much more functionality to it I don't think, but will 
improve the presentation of it in the future.

The only requirements for running the tracker is Pygame. 
You can simply run main.py without any args.
It "should" work on windows, mac, and linux if you run from source.
'''

import pygame
import os
import itemtracker
import areatracker
import image
from constants import *
from settings import *

pygame.init()

os.environ["SDL_MOUSE_FOCUS_CLICKTHROUGH"] = "1"

WIN = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(TITLE)
pygame.display.set_icon(image.singleImage(ICON_PATH))

_itemTracker = itemtracker.ItemTracker(ITEM_TRACKER_SIZE, ITEM_TRACKER_POSITION, ITEM_DATA)
_areaTracker = areatracker.AreaTracker(AREA_TRACKER_SIZE, AREA_TRACKER_POSITION, NODE_DATA, NODE_COLORS, BACKGROUND_DATA, BASE_NODE_PATH, ARROW_PATH, TRASHCAN_PATH, TRASHCAN_POSITION, BOSS_PATHS, BOSS_DATA, BOSS_COLOR, AREA_TRACKER_BACKGROUND_IMAGE)

def main():
    clock = pygame.time.Clock()
    mouse = pygame.mouse
    isRunning = True

    while isRunning:
        clock.tick(FPS)
        mousePosition = mouse.get_pos()
        
        #check events and update trackers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                _itemTracker.handleClick((mousePosition[0] - _itemTracker.position[0], mousePosition[1] - _itemTracker.position[1]))
                if mouse.get_pressed()[0]:
                    _areaTracker.handleLeftClick((mousePosition[0] - _areaTracker.position[0], mousePosition[1] - _areaTracker.position[1]))
                elif mouse.get_pressed()[1]:
                    _areaTracker.handleMiddleClick((mousePosition[0] - _areaTracker.position[0], mousePosition[1] - _areaTracker.position[1]))
                elif mouse.get_pressed()[2]:
                    _areaTracker.handleRightClick((mousePosition[0] - _areaTracker.position[0], mousePosition[1] - _areaTracker.position[1]))
                
        #clear screen and draw trackers
        WIN.fill(TRANSPARENT)
        _itemTracker.draw((mousePosition[0] - _itemTracker.position[0], mousePosition[1] - _itemTracker.position[1]))
        _areaTracker.draw((mousePosition[0] - _areaTracker.position[0], mousePosition[1] - _areaTracker.position[1]))
        WIN.blit(_itemTracker, _itemTracker.position)
        WIN.blit(_areaTracker, _areaTracker.position)

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()