"""the Menu class"""

import pygame as pg

from .settings_for_menu import *
from pygame import mixer

class Menu:
    pg.init()
    def __init__(self):
        self.displayed = True
        self.screen = pg.display.set_mode((0, 0), pg.NOFRAME)
        pg.display.toggle_fullscreen()
        self.font = pg.font.SysFont('Constantia', 75)  # if we're not changing the font, move it to Menu class
        self.font2 = pg.font.SysFont('Constantia', 50)
        self.font3 = pg.font.SysFont('Constantia', 28)
        self.current = "Main"
        self.background = background_main_menu  # if we're not changing the bg for menus, move it to Menu class
        self.mid_width = (self.screen.get_width() // 2) - (WIDTH_BUTTON // 2)
        self.mid_height = (self.screen.get_height() // 2) - (1.5 * HEIGHT_BUTTON)
        self.start = False
        self.load = False
        self.save = False
        self.volume = 0
        self.pause = False
    

    def draw_cursor(self):
        pass

    def blit_screen(self):
        pass



