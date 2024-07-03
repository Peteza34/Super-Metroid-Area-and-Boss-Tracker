#RGBA
BLACK = (0, 0, 0, 255)
BLACKISH = (30, 30, 30, 255)
WHITISH = (242, 242, 242, 255)
WHITE = (255, 255, 255, 255)
LIGHT_GRAY = (192, 192, 192, 255)
GRAY = (128, 128, 128, 255)
DARK_GRAY = (64, 64, 64, 255)
TRANSPARENT = (0, 0, 0, 0)

FPS = 20
ORIGIN = (0, 0)
MARGIN = 16

BOSS_NODE_WIDTH = 32
BOSS_DIM_PERCENT = 50

TRASHCAN_WIDTH = 32
TRASHCAN_POSITION = (596, 596) #relative to area tracker
TRASHCAN_DIM_PERCENT = 5
TRASHCAN_BRIGHTEN_AMOUNT = 16

ITEM_WIDTH = 64
ITEM_SPACING = 24
ITEM_COUNT = (7, 2) #(columns, rows)
ITEM_TRACKER_SIZE = (ITEM_COUNT[0] * (ITEM_SPACING + ITEM_WIDTH) + ITEM_SPACING, ITEM_COUNT[1] * (ITEM_SPACING + ITEM_WIDTH) + ITEM_SPACING)
ITEM_TRACKER_POSITION = (MARGIN, MARGIN)

AREA_TRACKER_SIZE = (640, 640)
AREA_TRACKER_POSITION = (MARGIN, ITEM_TRACKER_POSITION[1] + ITEM_TRACKER_SIZE[1] + 2 * MARGIN)
AREA_NODE_WIDTH = 26

STATUS_BAR_SIZE = (640 + 2 * MARGIN, 24)
STATUS_BAR_POSITION = (0, AREA_TRACKER_POSITION[1] + AREA_TRACKER_SIZE[1] + MARGIN)
STATUS_BAR_COLOR = BLACKISH
STATUS_FONT_PATH = ("fonts", "super-metroid.ttf")
STATUS_FONT_SIZE = 12

RESET_POSITION = ((16, STATUS_BAR_SIZE[1] // 2))
CONFIG_POSITION = ((STATUS_BAR_SIZE[0] - STATUS_BAR_SIZE[1] // 2 - 4, STATUS_BAR_SIZE[1] // 2)) #relative to status bar
CONFIG_BRIGHTEN_AMOUNT = 64

TITLE = "SM Area Rando Tracker"
WINDOW_SIZE = (AREA_TRACKER_SIZE[0] + 2 * MARGIN, AREA_TRACKER_SIZE[1] + ITEM_TRACKER_SIZE[1] + STATUS_BAR_SIZE[1] + 4 * MARGIN)
WINDOW_OFFSET = (1920 - WINDOW_SIZE[0], 30)

#RGB
LINE_COLORS = [(52, 124, 240),
                (95, 169, 23),
                (251, 104, 1),
                (100, 118, 134),
                (109, 135, 99),
                (121, 59, 62),
                (241, 163, 9),
                (229, 20, 0)]
LINE_COLORS_COUNT = len(LINE_COLORS)
LINE_WIDTH = 5 #int >= 1

#(Name, fill color RGBA)
NODE_COLORS = (("unlinked", (0, 255, 0, 255)),
                    ("normal", (215, 215, 255, 255)),
                    ("heat", (211, 82, 52, 255)), #(216, 53, 8, 255)
                    ("water", (155, 71, 178, 255)), #(182, 32, 216, 255)
                    ("inactive", (200, 200, 200, 0)))

#(Name, Center Position, type)
NODE_DATA = (("Gr Brin - Elevator", (71, 48), "normal"),
            ("Gr Brin - Meme Route", (119, 128), "normal"),
            ("Gr Brin - Noob Bridge", (167, 176), "normal"),
            ("Crat - Mushroom", (215, 112), "normal"),
            ("Crat - Tourian Entrance", (279, 112), "normal"),
            ("Crat - Meme Route", (311, 176), "normal"),
            ("Crat - Moat", (407, 64), "normal"),
            ("Crat - Crab Room", (375, 96), "normal"),
            ("WS - West Ocean", (471, 48), "normal"),
            ("WS - Forgotten Highway", (599, 96), "normal"),
            ("Red Brin - Elevator", (103, 240), "normal"),
            ("Red Brin - Mar Top Exit", (135, 272), "normal"),
            ("Red Brin - Middle", (39, 320), "normal"),
            ("Red Brin - Tube", (119, 336), "normal"),
            ("Red Brin - Mar Bottom Exit", (183, 336), "normal"),
            ("Red Brin - Bottom Right", (183, 368), "normal"),
            ("W Mar - Fish Room", (295, 256), "water"),
            ("W Mar - Crab Shaft", (375, 288), "water"),
            ("W Mar - Main Street", (295, 384), "water"),
            ("W Mar - Map Station", (343, 400), "water"),
            ("E Mar - Aqueduct", (471, 272), "water"),
            ("E Mar - Elevator", (599, 224), "water"),
            ("Kraid's Lair", (455, 384), "normal"),
            ("Tourian", (71, 448), "normal"),
            ("Croc's Lair", (119, 544), "normal"),
            ("UN - Elevator Left", (263, 480), "normal"),
            ("UN - Elevator Right", (327, 480), "normal"),
            ("UN - Croc Entrance", (295, 560), "heat"),
            ("UN - LN Entrance", (343, 560), "heat"),
            ("UN - LN Exit", (407, 496), "heat"),
            ("LN - Lava Dive", (503, 496), "heat"),
            ("LN - Three Musketeers", (567, 480), "heat"))

BOSS_DATA = (("Kraid's Lair Boss" , (583, 384)),
            ("Wrecked Ship Boss", (535, 112)),
            ("Maridia Boss", (535, 208)),
            ("Lower Norfair Boss", (535, 576)))

BOSS_PATHS = (("images", "bossnode.png"),
                ("images", "g4.png"),
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

#(directory, filename)
ICON_PATH = ("images", "croc.png")
BASE_NODE_PATH = ("images", "basenode.png")
ARROW_PATH = ("images", "arrow.png")
TRASHCAN_PATH = ("images", "trashcan.png")
AREA_MAP_PATH = ("images", "areamap.png")
BACKGROUND_PATH = ("images", "background.png")
CONFIG_PATH = ("images", "config.png")
RESET_PATH = ("images", "reset.png")
MENU_FONT_PATH = ("fonts", "super-metroid.ttf")
MENU_BACKGROUND_PATH = ("images", "menubackground.png")
EXIT_IMAGE_PATH = ("images", "exit.png")

#(name, grid position, path, isThreeTiered) since charge has special cases to handle starter charge
ITEM_DATA = (("Morph Ball", (0, 0), ("images", "items", "morph.png"), False), 
                ("Bombs", (1, 0), ("images", "items", "bombs.png"), False),
                ("Spring Ball", (2, 0), ("images", "items", "springball.png"), False),
                ("High Jump", (3, 0), ("images", "items", "hijump.png"), False),
                ("Speed Booster", (4, 0), ("images", "items", "speed.png"), False),
                ("Space Jump", (5, 0), ("images", "items", "space.png"), True),     # double jump
                ("Screw Attack", (6, 0), ("images", "items", "screw.png"), False),
                ("Charge Beam", (0, 1), ("images", "items", "charge.png"), True),   # starter charge
                ("Ice Beam", (1, 1), ("images", "items", "ice.png"), False),        # swapped order of ice and wave because heck u peteza
                ("Wave Beam", (2, 1), ("images", "items", "wave.png"), False),
                ("Spazer Beam", (3, 1), ("images", "items", "spazer.png"), False),
                ("Plasma Beam", (4, 1), ("images", "items", "plasma.png"), False),
                ("Varia Suit", (5, 1), ("images", "items", "varia.png"), True),     # heat shield
                ("Gravity Suit", (6, 1), ("images", "items", "gravity.png"), True)) # pressure valve

ITEM_DIM_PERCENT = 5
ITEM_DIM_PERCENT_INACTIVE = 65
ITEM_BRIGHTEN_AMOUNT = 18
ITEM_BRIGHTEN_AMOUNT_INACTIVE = 12

#(text, position(relative to menu panel))
SETTINGS_DATA = (("Background Image", (416, 51)),
                ("Suit Indicators", (416, 141)),
                ("Info Bar", (416, 231)),
                ("Multicolored Lines", (416, 321)))
MENU_IMAGE_PATHS = (("images", "optionactive.png"),
                    ("images", "optioninactive.png"))
MENU_OPTION_WIDTH = 48
MENU_TEXT_SIZE = 18
MENU_TEXT_XOFFSET = -360
MENU_EXIT_POSITION = (416, 411) # relative to menu
MENU_SIZE = (512, 512)
MENU_POSITION = (AREA_TRACKER_POSITION[0] + 64, AREA_TRACKER_POSITION[1] + 62)

#(text, position(relative to reset panel))
RESET_DATA = (("Reset the tracker?", (40, 70)),
              ("This cannot be undone.", (40, 140)),
              ("Yes", (90,269)),
              ("No", (375,269)))

RESET_MENU_SIZE = (512, 400)
RESET_EXIT_POSITION = (368, 299) # relative to reset panel
RESET_CHECK_POSITION = (96,299) # relative to reset panel
RESET_MENU_POSITION = (AREA_TRACKER_POSITION[0] + 64, AREA_TRACKER_POSITION[1] + 90)
RESET_BACKGROUND_PATH = (("images","resetbackground.png"))
RESET_CHECK_PATH = (("images","checkmark.png"))