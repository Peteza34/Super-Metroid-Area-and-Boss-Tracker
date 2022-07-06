import pygame
import image
from enum import Enum
from constants import *

def initAreaNodes(data):
    nodes = {}
    for entry in data:
        nodes[entry[0]] = AreaNode(entry[0], entry[1], entry[2])
    return nodes

def initBossNodes(data):
    return [BossNode(entry[0], entry[1]) for entry in data]

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

def initBossImages(bossPaths):
    images = {}
    baseImage = image.singleImage(bossPaths[0])
    
    #default bossNode images
    imageDefault = image.addBackground(image.changeColor(baseImage.copy(), WHITISH, TRANSPARENT), image.singleImage(bossPaths[1]))
    imageDefaultHighlight = image.changeColor(imageDefault.copy(), BLACKISH, GRAY)
    images["default"] = imageDefault
    images["defaultHighlight"] = imageDefaultHighlight

    #default inactive bossNode images
    imageInactive = image.changeColor(baseImage.copy(), WHITISH, TRANSPARENT)
    imageInactiveHighlight = image.changeColor(imageInactive.copy(), BLACKISH, GRAY)
    images["defaultInactive"] = imageInactive
    images["defaultInactiveHighlight"] = imageInactiveHighlight

    #construct the boss images for each of the 4 bosses
    for entry in bossPaths[2:]:
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

class Trashcan:
    def __init__(self, position, imagePath):
        self.position = position
        self.image = image.dimImage(image.singleImage(imagePath), TRASHCAN_DIM_PERCENT)
        self.highlightImage = image.brightenImage(self.image.copy(), TRASHCAN_BRIGHTEN_AMOUNT)
        self.rect = self.image.get_rect(center = position)

    def __str__(self):
        return "Trash Can"

class AreaNode:
    def __init__(self, name, position, nodeType):
        self.name = name
        self.position = position
        self.rect = pygame.Rect(position[0] - AREA_NODE_WIDTH // 2, position[1] - AREA_NODE_WIDTH // 2, AREA_NODE_WIDTH, AREA_NODE_WIDTH)
        self.isActive = True
        self.isLinked = False
        self.nodeType = nodeType
        self.linkType = "normal"

    def __str__(self):
        return self.name

class BossNode:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.rect = pygame.Rect(position[0] - BOSS_NODE_WIDTH // 2, position[1] - BOSS_NODE_WIDTH // 2, BOSS_NODE_WIDTH, BOSS_NODE_WIDTH)
        self.isActive = True
        self.bossIndex = 0

    def __str__(self):
        s = self.name
        if self.bossIndex > 0:
            s = s + " - " + BOSS_POOL[self.bossIndex].capitalize()
        return s

class Link:
    def __init__(self, nodes, color):
        self.nodes = nodes
        self.isActive = True
        self.color = color

    def toggleActive(self, isActive):
        self.isActive = isActive
        for node in self.nodes:
            node.isActive = isActive

    def toString(self, node = None):
        if not node:
            node = self.nodes[0]
        return str(node) + " ==> " + str(self.nodes[1] if node == self.nodes[0] else self.nodes[0])

#Indicates a link that has been initiated
class ClickState(Enum):
    NORMAL = 1
    PRIMED = 2

#Handles all of the logic and presentation of the area tracker
#It is a Pygame Surface, so essentially a drawing canvas for the tracker
class AreaTracker(pygame.Surface):
    def __init__(self, size, position, nodeData, nodeVarieties, areaMapPath, baseNodePath, arrowPath, trashcanPath, trashcanPosition, bossNodePaths, bossNodeData, settingsObj):
        super().__init__(size, flags = pygame.SRCALPHA)
        self.position = position
        self.rect = self.get_rect(topleft = position)
        self.links = {}
        self.nodes = initAreaNodes(nodeData)
        self.nodeImages = initAreaImages(nodeVarieties, baseNodePath)
        self.background = image.singleImage(areaMapPath)
        self.arrow = image.singleImage(arrowPath)
        self.trashcan = Trashcan(trashcanPosition, trashcanPath)
        self.bossNodes = initBossNodes(bossNodeData)
        self.bossImages = initBossImages(bossNodePaths)
        self.clickState = ClickState.NORMAL
        self.lastNode = None
        self.lineIndex = 0
        self.settingsObj = settingsObj

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

    def removeLink(self, node):
        if node in self.links:
            for n in self.links[node].nodes:
                self.links.pop(n)
                n.isLinked = False
                n.linkType = "normal"

    #updates the various tracker components, returns mouse hover message
    def update(self, mousePos, click):
        message = ""
        
        for areaNode in self.nodes.values():
            if areaNode.rect.collidepoint(mousePos):
                message = str(areaNode) if not areaNode.isLinked else self.links[areaNode].toString(areaNode)
                if click[0]: #left click
                    if self.clickState == ClickState.PRIMED and areaNode != self.lastNode:
                        self.addLink(self.lastNode, areaNode)
                    elif self.clickState == ClickState.NORMAL:
                        if areaNode in self.links:
                            self.links[areaNode].toggleActive(not areaNode.isActive)
                        else:
                            areaNode.isActive = not areaNode.isActive
                    self.clickState = ClickState.NORMAL
                elif click[2]: #right click
                    self.clickState = ClickState.PRIMED
                    self.lastNode = areaNode  
                elif click[1]: #middle click
                    self.clickState = ClickState.NORMAL
                break

        for bossNode in self.bossNodes:
            if bossNode.rect.collidepoint(mousePos):
                message = str(bossNode)
                if click[0]: #left click
                    if self.clickState == ClickState.NORMAL:
                        bossNode.isActive = not bossNode.isActive
                elif click[2]: #right click
                    bossNode.bossIndex = (bossNode.bossIndex + 1) % BOSS_COUNT
                if any(click):
                    self.clickState = ClickState.NORMAL
                break

        if self.trashcan.rect.collidepoint(mousePos) and self.clickState == ClickState.PRIMED:
            message = str(self.trashcan)
            if click[0]:
                self.removeLink(self.lastNode)
            if any(click):
                self.clickState = ClickState.NORMAL
        
        if not message and any(click):
            self.clickState = ClickState.NORMAL

        return message

    # Clears the canvas and draws all of the different components
    def draw(self, mousePosition):
        self.fill(TRANSPARENT)
        self.blit(self.background, ORIGIN)
        
        for node in self.nodes.values():
            key = "inactive" if not node.isActive else "unlinked" if not node.isLinked else "normal" if not self.settingsObj.checkOption("Suit Indicators") else node.linkType
            if node.rect.collidepoint(mousePosition):
                key = key + "Highlight"

            self.blit(self.nodeImages[key], node.rect)

            if self.clickState == ClickState.PRIMED and self.lastNode == node:
                self.blit(self.arrow, node.rect)

        for bossNode in self.bossNodes:
            key = BOSS_POOL[bossNode.bossIndex]
            if not bossNode.isActive:
                key = key + "Inactive"

            if bossNode.rect.collidepoint(mousePosition):
                key = key + "Highlight"

            self.blit(self.bossImages[key], bossNode.rect)

        if self.clickState == ClickState.PRIMED:
            self.blit(self.trashcan.highlightImage if self.trashcan.rect.collidepoint(mousePosition) else self.trashcan.image, self.trashcan.rect)

        for link in set(self.links.values()):
            color = DARK_GRAY if not link.isActive else LINE_COLORS[0] if not self.settingsObj.checkOption("Multicolored Lines") else link.color
            lineWidth = LINE_WIDTH if link.isActive else min(LINE_WIDTH, 2)
            pygame.draw.line(self, color, link.nodes[0].position, link.nodes[1].position, lineWidth)

    #Resets the tracker to initial state. Not used atm
    def resetTracker(self):
        for node in self.nodes.values():
            self.removeLink(node)
            node.isActive = True
            node.linkType = "normal"

        for bossNode in self.bossNodes:
            bossNode.isActive = True
            bossNode.bossIndex = 0            