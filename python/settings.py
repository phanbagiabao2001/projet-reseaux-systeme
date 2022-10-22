from os import path
import pygame as pg

TILE_SIZE = 64
TILE_SIZE_MINI_MAP = 4
MAP_SIZE = 50
STARTING_POS1 = (int(0.8 * MAP_SIZE), int(0.1 * MAP_SIZE))
STARTING_POS2 = (int(0.4 * MAP_SIZE-2), int(0.8 * MAP_SIZE-2))

STARTING_RESOURCES_SAND = [2000, 2000, 1000, 2000]
STARTING_RESOURCES = [10000, 200000, 1000, 90000]
STARTING_RESOURCES_AI = [2000, 400, 200, 400]

# Buttons
HEIGHT_BUTTON = 50
WIDTH_BUTTON = 250
GAP = 75      # gap between the buttons
FONT_SIZE = 15

# Chat box
COLOR_INACTIVE = pg.Color('#808000')
COLOR_ACTIVE = pg.Color('#ffff00')

# Health Bar
HEALTH_BAR_LENGTH_BUILDING = 150
HEALTH_BAR_LENGTH_UNIT = 50

# colors
FOG_BLACK = -1
FOG_GREY = 0
FOG_NONE = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238, 130, 238)
MARRON = (165, 42, 42)
BURGUNDY = (179, 57, 57)
GOLD = (255, 215, 200)
YELLOW_LIGHT = (249, 231, 159)
BEIGE = (255, 253, 208)
GREEN_DARK = (9, 48, 22)
BLUE_SKY = (122, 215, 255)
PINK = (255, 88, 150)
PURPLE = (128, 0, 128)
MINI_MAP_COLOUR = (64, 64, 64, 32)
GUI_COLOUR = (87, 65, 47, 200)
GUI_BORDER_COLOR = (88, 41, 0, 255)
GUI_MINIMAP_COLOUR = (0, 0, 0, 200)
# GUI_COLOUR = (198, 155, 93, 175)

CONSTRUCTION = 1
DESTROY = 0

check_destroy = False

# Paths definitions
# Gameplay folder
AOE_folder = path.dirname(__file__)  # Path of the Project_Python_AoE folder
graphics_folder = path.join(AOE_folder, "assets/graphics")  # Path for graphics
AI_action_JSONfile = path.join(AOE_folder, "game/AI_action.json")

# map's ressource
Tree_img = pg.transform.scale(pg.image.load(path.join(graphics_folder, "tree.png")), (125, 105))
Rock_img = pg.transform.scale(pg.image.load(path.join(graphics_folder, "rock2.png")), (100, 100))
Gold_img = pg.transform.scale(pg.image.load(path.join(graphics_folder, "gold.png")), (100, 100))
Bush_img = pg.transform.scale(pg.image.load(path.join(graphics_folder, "bush.png")), (80, 80))
Block_img = pg.transform.scale(pg.image.load(path.join(graphics_folder, "block_aoe.png")), (143, 150))
Water_img = pg.transform.scale(pg.image.load(path.join(graphics_folder, "water.png")), (125, TILE_SIZE))
wood_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "wood_icon.png")), (35, 25))
rock_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "rock_icon.png")), (35, 25))
gold_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "gold_icon.png")), (35, 25))
food_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "food_icon.png")), (35, 25))

# buildings
firstage_towncenter = pg.transform.scale(pg.image.load(path.join(graphics_folder, "firstage_towncenter.png")),
                                         (143, 128))
firstage_barracks = pg.transform.scale(pg.image.load(path.join(graphics_folder, "firstage_barracks.png")), (143, 128))
firstage_archery = pg.transform.scale(pg.image.load(path.join(graphics_folder, "firstage_archery.png")), (143, 128))
secondage_towncenter = pg.transform.scale(pg.image.load(path.join(graphics_folder, "secondage_towncenter.png")),
                                          (143, 128))
secondage_barracks = pg.transform.scale(pg.image.load(path.join(graphics_folder, "secondage_barracks.png")), (143, 128))
secondage_archery = pg.transform.scale(pg.image.load(path.join(graphics_folder, "secondage_archery.png")), (143, 128))
stable = pg.transform.scale(pg.image.load(path.join(graphics_folder, "stable.png")), (143, 128))
towncenter_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "towncenter_icon.png")), (143, 128))
barracks_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "barracks_icon.png")), (143, 128))
archery_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "archery_icon.png")), (143, 128))
stable_icon = pg.transform.scale(pg.image.load(path.join(graphics_folder, "stable_icon.png")), (143, 128))

# units
archer = pg.transform.scale(pg.image.load(path.join(graphics_folder, "archer.png")), (30, 40))
infantryman = pg.transform.scale(pg.image.load(path.join(graphics_folder, "pikeman.png")), (38, 48))
villager = pg.transform.scale(pg.image.load(path.join(graphics_folder, "villager.png")), (30, 40))
cavalier = pg.transform.scale(pg.image.load(path.join(graphics_folder, "cavalier.png")), (45, 55))
supra = pg.transform.scale(pg.image.load(path.join(graphics_folder, "supra.png")), (75, 105))

# menu
menuf = path.dirname(__file__)  # Path of the Project_Python_AoE foler
data_image = path.join(menuf, "menu/data/bg_imgs")  # Path for graphic
data_font = path.join(menuf, "menu/data/font/trajan-pro")

background_main_menu = pg.transform.scale(pg.image.load(path.join(data_image, "backgroundaoe4.png")), (1920, 1080))
trajan = path.join(data_font, "TrajanPro.ttf")

# save game
save_map = path.join(AOE_folder, "Save_game/save_map.json")
save_entities = path.join(AOE_folder, "Save_game/save_entities.json")
save_units = path.join(AOE_folder, "Save_game/save_units.json")
