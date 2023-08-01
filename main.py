'''
This is an area and boss tracker that is meant to be used for area randomizer modes
of the Super Metroid VARIA Randomizer. It is simpler than the one on the VARIA website, 
but is designed to be compact so you can place it alongside a windowed emulator on the
same monitor. 

The only requirements for running the tracker is Pygame. 
You can simply run main.py without any args.
It "should" work on windows, mac, and linux if you run from source.
'''

import pygame
import os
import trackercore
import image
from constants import *
from settings import *

os.environ["SDL_MOUSE_FOCUS_CLICKTHROUGH"] = "1" #allows mouse click events when window is not in focus
os.environ["SDL_VIDEO_WINDOW_POS"] = str(WINDOW_OFFSET[0]) + "," + str(WINDOW_OFFSET[1]) #starting position for the window

pygame.init()

WIN = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(TITLE)
pygame.display.set_icon(image.singleImage(ICON_PATH))

_trackerCore = trackercore.TrackerCore(WINDOW_SIZE, image.singleImage(BACKGROUND_PATH))

def main():
    clock = pygame.time.Clock()
    mouse = pygame.mouse
    isRunning = True

    newSize = WINDOW_SIZE

    while isRunning:
        clock.tick(FPS)
        click = [0, 0, 0] #[left click, middle click, right click]
        mousePos = mouse.get_pos()
        mousePos = (mousePos[0] * WINDOW_SIZE[0] / newSize[0], mousePos[1] * WINDOW_SIZE[1] / newSize[1])

        #check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = mouse.get_pressed()[:3]
            if event.type == pygame.VIDEORESIZE:
                newSize = event.dict['size']

        #update trackers
        _trackerCore.update(mousePos, click)
                
        #clear screen and draw trackers
        WIN.fill(TRANSPARENT)
        _trackerCore.draw(mousePos)
        WIN.blit(pygame.transform.scale(_trackerCore, newSize), ORIGIN)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()