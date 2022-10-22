from os import path
import pygame as pg

# Buttons
HEIGHT_BUTTON = 50
WIDTH_BUTTON = 250
GAP = 75      # gap between the buttons
FONT_SIZE = 15

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

# menu
menuf = path.dirname(__file__)  # Path of the Project_Python_AoE foler
data_image = path.join(menuf, "data/bg_imgs")  # Path for graphic
data_font = path.join(menuf, "data/font/trajan-pro")

background_main_menu = pg.transform.scale(pg.image.load(path.join(data_image, "backgroundaoe4.png")), (1920, 1080))