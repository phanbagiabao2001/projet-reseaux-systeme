"""Credits screen"""
from os import path
from time import sleep
from config.colors import BEIGE, YELLOW_LIGHT, BLACK, BLUE_GREY
from config.window import HEIGHT, WIDTH
import pygame as pg
import json
from window import _Elements
from config.buttons import HEIGHT_BUTTON, HEIGHT_SLIDER, WIDTH_BUTTON, WIDTH_SLIDER
from config.screens import BACKGROUND_CREDITS, CREDITS, MENU, NEW_GAME, OPTIONS, LOAD_GAME, MENU, NEW_GAME, CHARACTER_CREATION, TRANSITION_OUT
from itertools import cycle
from logger import logger
from pygame_widgets import TextBox
from typing import Text
from tkinter import *
from py_to_C import py_to_c, is_online


class OnlineGame(_Elements):
    """Credit screen"""

    def __init__(self):
        self.name = CREDITS
        self.next = MENU
        super(OnlineGame, self).__init__(self.name, self.next, 'load_game', 'background.jpg', {})

        self.background = pg.Surface((WIDTH, HEIGHT))
        self.new()

    def new(self):
        image = pg.image.load(
            path.join(
                self.img_folder,
                'load_game',
                'background.jpg')).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))

        self.btns_dict = self.create_buttons_dict()
        self.create_buttons(self.image, start_y_offset=8 * HEIGHT // 10)
        self.create_text_box()
        self.create_port_d_box()
        self.create_port_e_box()
        self.create_port_r_box()
        self.create_port_l_box()
        self.create_player_nb_box()
        self.create_back_button(self.image, self.load_next_state, [MENU])
        self.text_port_r.setText("65535")
        self.text_port_e.setText("65534")
        self.text_port_d.setText("65432")
        self.text_port_l.setText("65532")
        self.text_name.setText("127.0.0.1")


    
    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "confirm": {
                "text": "confirm",
                "on_click": self.when_confirmed,
                "on_click_params": [CHARACTER_CREATION],
            }
        }
    

    def when_confirmed(self, state):
        py_to_c.addr = self.text_name.getText()
        py_to_c.D_port = int(self.text_port_d.getText())
        py_to_c.L_port = int(self.text_port_l.getText())
        py_to_c.R_port = int(self.text_port_r.getText())
        py_to_c.E_port = int(self.text_port_e.getText())
        py_to_c.currentPlayer = int(self.text_player_nb.getText())
        is_online.setOnline()

        logger.info("ip is : " + self.text_name.getText() + " and distant port is : " + self.text_port_d.getText())

        py_to_c.connect()
        self.load_next_state(LOAD_GAME)


 
    def create_text_box(self):
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        _y = 3 * HEIGHT // 10 - HEIGHT_BUTTON //2 -25
        self.text_name = TextBox(self.background, _x, _y, WIDTH_BUTTON, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, radius=10, borderThickness=4)
                        
    def create_port_r_box(self):
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        _y = 3 * HEIGHT // 10 - HEIGHT_BUTTON // 2 +50
        self.text_port_r = TextBox(self.background, _x, _y, WIDTH_BUTTON, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, radius=10, borderThickness=4)

    def create_port_e_box(self):
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        _y = 3 * HEIGHT // 10 - HEIGHT_BUTTON // 2 +125
        self.text_port_e = TextBox(self.background, _x, _y, WIDTH_BUTTON, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, radius=10, borderThickness=4)

    def create_port_l_box(self):
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        _y = 3 * HEIGHT // 10 - HEIGHT_BUTTON // 2 +200
        self.text_port_l = TextBox(self.background, _x, _y, WIDTH_BUTTON, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, radius=10, borderThickness=4)
                            
    def create_port_d_box(self):
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        _y = 3 * HEIGHT // 10 - HEIGHT_BUTTON // 2 +275
        self.text_port_d = TextBox(self.background, _x, _y, WIDTH_BUTTON, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, radius=10, borderThickness=4)

    def create_player_nb_box(self):
        _x =  WIDTH // 10 - WIDTH_BUTTON // 14
        _y = 2 * HEIGHT // 10 - HEIGHT_BUTTON // 2 + 75
        self.text_player_nb = TextBox(self.background, _x, _y, WIDTH_BUTTON//7, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, radius=10, borderThickness=4)

    


    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        super().events_buttons(back=True)
        self.draw()

    def all_events(self, events):
        self.text_name.listen(events)
        self.text_port_d.listen(events)
        self.text_port_e.listen(events)
        self.text_port_l.listen(events)
        self.text_port_r.listen(events)
        self.text_player_nb.listen(events)
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.load_next_state(MENU)


    def draw(self):
        """Draw content"""
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image, (0, 0))
        self.text_name.draw()
        self.text_port_d.draw()
        self.text_port_e.draw()
        self.text_port_l.draw()
        self.text_port_r.draw()
        self.text_player_nb.draw()
        self.draw_text("Enter the Ip address", self.text_font, 24, BEIGE, WIDTH //
                       2, 3 * HEIGHT // 10 - 75 , align="n", screen=self.background)
        self.draw_text("Enter two available ports", self.text_font, 24, BEIGE, WIDTH //
                       2, 3 * HEIGHT // 10   , align="n", screen=self.background)
        self.draw_text("Enter your local port", self.text_font, 24, BEIGE, WIDTH //
                       2, 3 * HEIGHT // 10 + 150, align="n", screen=self.background)
        self.draw_text("Enter your distant port", self.text_font, 24, BEIGE, WIDTH //
                       2, 3 * HEIGHT // 10 + 225, align="n", screen=self.background)

        self.text_player_nb.draw()
        self.draw_text("Player id", self.text_font,24, BEIGE, WIDTH//10,2 * HEIGHT // 10,align="n",screen=self.background)
        
        super().draw_elements("connect", back=True)



