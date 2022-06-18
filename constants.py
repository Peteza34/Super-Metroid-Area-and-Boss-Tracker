from settings import *

#RGBA
BLACK = (0, 0, 0, 255)
BLACKISH = (30, 30, 30, 255)
WHITISH = (242, 242, 242, 255)
GRAY = (128, 128, 128, 255)
DARK_GRAY = (64, 64, 64, 255)
TRANSPARENT = (0, 0, 0, 0)

FPS = 20
ORIGIN = (0, 0)

BOSS_NODE_WIDTH = 32
BOSS_DIM_PERCENT = 50

TRASHCAN_WIDTH = 32
TRASHCAN_POSITION = (599, 583) #relative to area tracker
TRASHCAN_DIM_PERCENT = 10

ITEM_WIDTH = 64
ITEM_SPACING = 24
ITEM_COUNT = (7, 2)
ITEM_TRACKER_SIZE = (ITEM_COUNT[0] * (ITEM_SPACING + ITEM_WIDTH) + ITEM_SPACING, ITEM_COUNT[1] * (ITEM_SPACING + ITEM_WIDTH) + ITEM_SPACING)
ITEM_TRACKER_POSITION = ORIGIN

AREA_TRACKER_SIZE = (638, 622)
AREA_TRACKER_POSITION = (0, ITEM_TRACKER_POSITION[1] + ITEM_TRACKER_SIZE[1])
AREA_NODE_WIDTH = 26

TITLE = "SM Area Rando Tracker"
WINDOW_SIZE = (640, AREA_TRACKER_SIZE[1] + ITEM_TRACKER_SIZE[1])


LINE_COLORS_COUNT = len(LINE_COLORS)

#(Name, fill color RGBA)
NODE_COLORS = (("unlinked", (0, 255, 0, 255)),
                    ("normal", (215, 215, 255, 255)),
                    ("heat", (216, 53, 8, 255)),
                    ("water", (182, 32, 216, 255)),
                    ("inactive", (200, 200, 200, 0)))

#(Name, Center Position, type)
NODE_DATA = (("Gr Brin - Elevator", (71, 39), "normal"),
            ("Gr Brin - Meme Route", (119, 119), "normal"),
            ("Gr Brin - Noob Bridge", (167, 167), "normal"),
            ("Crat - Mushroom", (215, 87), "normal"),
            ("Crat - Tourian Entrance", (279, 87), "normal"),
            ("Crat - Meme Route", (311, 135), "normal"),
            ("Crat - Moat", (407, 39), "normal"),
            ("Crat - Crab Room", (375, 71), "normal"),
            ("WS - West Ocean", (471, 39), "normal"),
            ("WS - Forgotten Highway", (599, 87), "normal"),
            ("Red Brin - Elevator", (103, 231), "normal"),
            ("Red Brin - Maridia Top Exit", (135, 263), "normal"),
            ("Red Brin - Middle", (39, 311), "normal"),
            ("Red Brin - Tube", (119, 327), "normal"),
            ("Red Brin - Maridia Bottom Exit", (183, 327), "normal"),
            ("Red Brin - Bottom Right", (183, 359), "normal"),
            ("W Mar - Fish Room", (295, 231), "water"),
            ("W Mar - Crab Shaft", (375, 263), "water"),
            ("W Mar - Main Stret", (295, 359), "water"),
            ("W Mar - Map Station", (343, 359), "water"),
            ("E Mar - Aqueduct", (471, 263), "water"),
            ("E Mar - Elevator", (599, 215), "water"),
            ("Kraid", (471, 375), "normal"),
            ("Tourian", (71, 439), "normal"),
            ("Crocomire", (119, 535), "normal"),
            ("UN - Elevator Left", (263, 471), "normal"),
            ("UN - Elevator Right", (327, 471), "normal"),
            ("UN - Croc Entrance", (295, 551), "heat"),
            ("UN - LN Entrance", (343, 551), "heat"),
            ("UN - LN Exit", (407, 487), "heat"),
            ("LN - Lava Dive", (503, 487), "heat"),
            ("LN - Three Musketeers", (567, 487), "heat"))

BOSS_DATA = (("Kraid's Lair Boss" , (583, 375)),
            ("WS Boss", (535, 103)),
            ("Maridia Boss", (535, 199)),
            ("LN Boss", (535, 567)))

BOSS_PATHS = (("images", "bossnode.png"),
                ("images", "kraid.png"),
                ("images", "phantoon.png"),
                ("images", "draygon.png"),
                ("images", "ridley.png"))

BOSS_POOL = ("default",
             "kraid", 
             "phantoon", 
             "draygon", 
             "ridley")
BOSS_COUNT = len(BOSS_POOL)

BOSS_COLOR = (0, 176, 255, 255)

#(directory, filename)
ICON_PATH = ("images", "croc.png")
BASE_NODE_PATH = ("images", "basenode.png")
ARROW_PATH = ("images", "arrow.png")
TRASHCAN_PATH = ("images", "trashcan.png")

#(Background path, foreground path)
BACKGROUND_DATA = (("images", "background.png"),
                    ("images", "areamap.png"))

#(name, grid position, path)
ITEM_DATA = (("morph", (0, 0), ("images", "items", "morph.png")), 
                ("bombs", (1, 0), ("images", "items", "bombs.png")),
                ("spring", (2, 0), ("images", "items", "springball.png")),
                ("highjump", (3, 0), ("images", "items", "hijump.png")),
                ("speed", (4, 0), ("images", "items", "speed.png")),
                ("space", (5, 0), ("images", "items", "space.png")),
                ("screw", (6, 0), ("images", "items", "screw.png")),
                ("charge", (0, 1), ("images", "items", "charge.png")),
                ("wave", (1, 1), ("images", "items", "wave.png")),
                ("ice", (2, 1), ("images", "items", "ice.png")),
                ("spazer", (3, 1), ("images", "items", "spazer.png")),
                ("plasma", (4, 1), ("images", "items", "plasma.png")),
                ("varia", (5, 1), ("images", "items", "varia.png")),
                ("gravity", (6, 1), ("images", "items", "gravity.png")))

ITEM_DIM_PERCENT = 5
ITEM_DIM_PERCENT_INACTIVE = 65
ITEM_BRIGHTEN_AMOUNT = 18
ITEM_BRIGHTEN_AMOUNT_INACTIVE = 12