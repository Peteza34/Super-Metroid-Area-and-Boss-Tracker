import pygame
import image
from enum import Enum
from constants import *
from settings import *

#data = (name, location(x, y), type)
def initAreaNodes(data):
    nodes = {}
    for entry in data:
        nodes[entry[0]] = AreaNode(entry[0], entry[1], entry[2])
    return nodes

#data = (name, location(x, y))
def initBossNodes(data):
    return [BossNode(entry[0], entry[1]) for entry in data]

#data = (key(type of transition: heat, water, or normal), color(rgba))
#baseImagePath is a path to a template image used to construct our areanode images
def initAreaImages(data, baseImagePath):
    nodeImages = {}
    baseImage = image.singleImage(baseImagePath)
    for entry in data:
        #replace interior with color, border stays blackish
        imageA = image.changeColor(baseImage.copy(), WHITISH, entry[1])
        nodeImages[entry[0]] = imageA
        
        #replace blackish border with a highlilght color for mouse-hover images
        colorB = None
        if entry[0] == "heat" or entry[0] == "water":
            colorB = [min(255, val * 2) for val in entry[1]]
        else:
            colorB = [val // 3 * 2 for val in entry[1]]
        colorB[-1] = 255
        imageB = image.changeColorIgnoreAlpha(imageA.copy(), BLACKISH, colorB)
        nodeImages[entry[0] + "Highlight"] = imageB
    return nodeImages

#bossPaths = list of paths for the boss images and the template boss node
#The template node is assumed to be in index 0
#color = the default color of the interior of the boss nodes
def initBossImages(bossPaths, color):
    images = {}
    #Highlight color for the mouse-hover image of default bossNodes, derived from interior color
    baseImage = image.singleImage(bossPaths[0])
    colorB = [(val // 4 * 3) for val in color]
    colorB[-1] = 255
    
    #default bossNode images
    imageDefault = image.changeColor(baseImage.copy(), WHITISH, color)
    imageDefaultHighlight = image.changeColor(imageDefault.copy(), BLACKISH, colorB)
    images["default"] = imageDefault
    images["defaultHighlight"] = imageDefaultHighlight

    #default inactive bossNode images
    imageInactive = image.changeColor(baseImage.copy(), WHITISH, TRANSPARENT)
    imageInactiveHighlight = image.changeColor(imageInactive.copy(), BLACKISH, GRAY)
    images["defaultInactive"] = imageInactive
    images["defaultInactiveHighlight"] = imageInactiveHighlight

    #construct the boss images for each of the 4 bosses
    for entry in bossPaths[1:]:
        #create boss image and give it blackish border
        bossImage = image.addBackground(image.changeColor(baseImage.copy(), WHITISH, TRANSPARENT), image.singleImage(entry))
        key = entry[1][:-4] #parse filename without extension to use as key
        images[key] = bossImage

        #create dim boss image and give it blackish border for inactive image, gray border for inactive highlight image
        bossInactive = image.addBackground(image.changeColor(baseImage.copy(), WHITISH, TRANSPARENT), image.dimImage(image.singleImage(entry), BOSS_DIM_PERCENT))
        images[key + "Inactive"] = bossInactive
        bossInactive = image.addBackground(image.changeColor(image.changeColor(baseImage.copy(), WHITISH, TRANSPARENT), BLACKISH, GRAY), bossInactive.copy())
        images[key + "Inactive" + "Highlight"] = bossInactive

        #highlight image
        bossHighlight = image.changeColor(bossImage.copy(), BLACKISH, GRAY)
        images[key + "Highlight"] = bossHighlight
    return images

#data = path to background image
#will give it a plain black background if hasBackground = False
def initBackground(data, hasBackground = True):
    background = None
    if hasBackground:
        background = image.singleImage(data[0])
    return image.addBackground(image.singleImage(data[1]), background)

#Used for disposing of active transition links
class Trashcan:
    def __init__(self, position, imagePath):
        self.position = position
        self.image = image.dimImage(image.singleImage(imagePath), TRASHCAN_DIM_PERCENT)
        self.highlightImage = image.brightenImage(self.image.copy(), 15)
        self.rect = self.image.get_rect(center = position)

#Represents each area transition
class AreaNode:
    def __init__(self, name, position, nodeType):
        self.name = name
        self.position = position
        self.rect = pygame.Rect(position[0] - AREA_NODE_WIDTH // 2, position[1] - AREA_NODE_WIDTH // 2, AREA_NODE_WIDTH, AREA_NODE_WIDTH)
        self.isActive = True
        self.isLinked = False
        self.nodeType = nodeType
        self.linkType = "normal"

#Represents each boss location
class BossNode:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.rect = pygame.Rect(position[0] - BOSS_NODE_WIDTH // 2, position[1] - BOSS_NODE_WIDTH // 2, BOSS_NODE_WIDTH, BOSS_NODE_WIDTH)
        self.isActive = True
        self.bossIndex = 0

#Represents a link between two area transitions
class Link:
    def __init__(self, nodes, color):
        self.nodes = nodes
        self.isActive = True
        self.color = color

    def toggleActive(self, isActive):
        self.isActive = isActive
        for node in self.nodes:
            node.isActive = isActive

#PRIMED is the state after right clicking an area transition. 
#Left clicking a different transition while in the PRIMED state will create a link
class ClickState(Enum):
    NORMAL = 1
    PRIMED = 2

#Handles all of the logic and presentation of the area tracker
#It is a Pygame Surface, so essentially a drawing canvas for the program
class AreaTracker(pygame.Surface):
    def __init__(self, size, position, nodeData, nodeVarieties, backgroundData, baseNodePath, arrowPath, trashcanPath, trashcanPosition, bossNodePaths, bossNodeData, bossNodeColor,  hasBackgroundImage = True):
        super().__init__(size, flags = pygame.SRCALPHA)
        self.position = position
        self.links = {}
        self.nodes = initAreaNodes(nodeData)
        self.nodeImages = initAreaImages(nodeVarieties, baseNodePath)
        self.background = initBackground(backgroundData, hasBackgroundImage)
        self.arrow = image.singleImage(arrowPath)
        self.trashcan = Trashcan(trashcanPosition, trashcanPath)
        self.bossNodes = initBossNodes(bossNodeData)
        self.bossImages = initBossImages(bossNodePaths, bossNodeColor)
        self.clickState = ClickState.NORMAL
        self.lastNode = None
        self.lineIndex = 0

    #Removes any existing link from the two nodes, creates a link between the two, and assigns it a color from the pool of line colors
    #Changes the color of each node to represent heat or water when applicable
    def addLink(self, nodeA, nodeB):
        self.removeLink(nodeA)
        self.removeLink(nodeB)
        nodeA.isLinked = nodeB.isLinked = True
        nodeA.linkType = nodeB.nodeType
        nodeB.linkType = nodeA.nodeType
        self.links[nodeA] = self.links[nodeB] = Link([nodeA, nodeB], LINE_COLORS[self.lineIndex])
        self.lineIndex = (self.lineIndex + 1) % LINE_COLORS_COUNT

    #checks for an existing link and removes it
    def removeLink(self, node):
        if node in self.links:
            for n in self.links[node].nodes:
                self.links.pop(n)
                n.isLinked = False
                n.linkType = "normal"

    #Checks each node for mouse collision and performs an action on it, depending on the state of the tracker
    def handleLeftClick(self, mousePosition):
        #area node collision check
        for node in self.nodes.values():
            if node.rect.collidepoint(mousePosition):
                if self.clickState == ClickState.PRIMED and node != self.lastNode:
                    self.addLink(self.lastNode, node)
                elif self.clickState == ClickState.NORMAL:
                    if node in self.links:
                        self.links[node].toggleActive(not node.isActive)
                    else:
                        node.isActive = not node.isActive

        #boss node collision check
        for bossNode in self.bossNodes:
            if bossNode.rect.collidepoint(mousePosition) and self.clickState == ClickState.NORMAL:
                bossNode.isActive = not bossNode.isActive

        #trashcan collision check. Will remove a link from a node if in a PRIMED state
        if self.clickState == ClickState.PRIMED and self.trashcan.rect.collidepoint(mousePosition):
            self.removeLink(self.lastNode)

        #Every left click returns tracker to NORMAL state
        self.clickState = ClickState.NORMAL

    #Checks each node for mouse collision and performs an action on it, depending on the state of the tracker
    def handleRightClick(self, mousePosition):
        #boss node collision check. Will cycle through bosses if not in PRIMED state
        for bossNode in self.bossNodes:
            if bossNode.rect.collidepoint(mousePosition) and self.clickState == ClickState.NORMAL:
                bossNode.bossIndex = (bossNode.bossIndex + 1) % BOSS_COUNT

        self.clickState = ClickState.NORMAL

        #area node collision check. will "prime" the node and put tracker in "PRIMED" state
        for node in self.nodes.values():
            if node.rect.collidepoint(mousePosition):
                self.clickState = ClickState.PRIMED
                self.lastNode = node    

    #Every middle click will return tracker to NORMAL state. 
    #May add other middle click functionality in the future.
    def handleMiddleClick(self, mousePosition):
        self.clickState = ClickState.NORMAL

    # Clears the canvas and draws all of the different components
    def draw(self, mousePosition):
        self.fill(BLACKISH)
        self.blit(self.background, ORIGIN)
        
        #draw area nodes
        for node in self.nodes.values():
            #determine which node image to use
            key = "inactive" if not node.isActive else "unlinked" if not node.isLinked else node.linkType

            #check for mouse hover
            if node.rect.collidepoint(mousePosition):
                key = key + "Highlight"

            self.blit(self.nodeImages[key], node.rect)

            #Draw arrow on primed node if in PRIMED state
            if self.clickState == ClickState.PRIMED:
                if self.lastNode == node:
                    self.blit(self.arrow, node.rect)

        #draw boss nodes
        for bossNode in self.bossNodes:
            key = BOSS_POOL[bossNode.bossIndex]
            #check if bossnode is active
            if not bossNode.isActive:
                key = key + "Inactive"

            #check for mouse hover
            if bossNode.rect.collidepoint(mousePosition):
                key = key + "Highlight"

            self.blit(self.bossImages[key], bossNode.rect)

        #draw trashcan if PRIMED
        if self.clickState == ClickState.PRIMED:
            self.blit(self.trashcan.highlightImage if self.trashcan.rect.collidepoint(mousePosition) else self.trashcan.image, self.trashcan.rect)

        #draw all of the links
        for link in set(self.links.values()):
            color = link.color if link.isActive else DARK_GRAY
            lineWidth = LINE_WIDTH if link.isActive else min(LINE_WIDTH, 2)
            pygame.draw.line(self, color, link.nodes[0].position, link.nodes[1].position, lineWidth)

    #Resets the tracker to initial state. Not used yet but probably will be implemented
    def resetTracker(self):
        for node in self.nodes.values():
            self.removeLink(node)
            node.isActive = True
            node.linkType = "Normal"

        for bossNode in self.bossNodes:
            bossNode.isActive = True
            bossNode.bossIndex = 0            