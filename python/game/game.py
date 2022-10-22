import pygame as pg
import sys

from game.save_game import Load_game, Save_game

from .map import Map
from settings import *
from .utils import draw_text
from .camera import Camera
from .gui import Gui
from .resource import Resource
from .units import Archer, Infantryman, Villager
from .buildings import TownCenter
from .events import *
from .AI import *
from menu.all_menu import All_menus
from share_data import getRXQueue, getTXQueue, getRBQueue

class Game:

    # preparing the screen and coordinates for the game
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.real_game = False

        self.menu = All_menus()

        self.load = False
        self.loaded = False

        # event
        self.events = Event(clock, screen)

        # entities
        self.entities = []

        # resource
        self.resource_man = self.events.resource_man

        #chatbox
        self.chatbox = self.events.chatbox

        # gui
        self.gui = Gui(self.resource_man, self.width, self.height, self.events)

        # create the world with 50 by 50 grid
        self.map = Map(self.resource_man, self.entities, self.gui, MAP_SIZE, MAP_SIZE, self.width, self.height,
                       self.events)

        self.camera = Camera(self.width, self.height)

        self.game_time = Game_time()

        # self.AI = AI(self.game_time, self.map, self.resource_man)

        self.save_game = Save_game(self.map)

        self.load_game = Load_game(self.map)

        self.map.load_game = self.load_game

        self.menu.current = "Game"




    # running
    def run(self):
        if self.load and not self.loaded:
            self.events.Load_game = True
            self.loaded = True
            self.playing = False
        else:
            self.playing = True
        while self.playing:
            tick = self.clock.tick(60)  # Limiter le nombre de FPS à 60 (c'est déjà très bien)
            self.game_time.second += tick / 1000  # Compter le nombre de secondes écoulées depuis le lancement du jeu
            self.update()  # La fonction globale qui sert à mettre à jour sans arrêt l'état des unités, bâtiments etc...
            self.draw()  # Dessiner le GUI
            self.events.events()  # Démarre la boucle des évènements pour permettre de détecter toutes les actions dans le jeu

            if not self.real_game:
                # Lancer une vraie partie, ne pas oublier de mettre à jour les starting resources
                self.start_real_game()
                # self.AI.action_json()  # Dis à l'AI de commencer à jouer
            # else:
                # self.AI.action_json()


    def update(self):
       
        if getRBQueue().empty() == False : 
            coor = getRBQueue().get()      
            if int(coor[4]) != 0 : 
                # coor = getRXQueue().get()
                if coor[0] == 1:
                    self.map.updateBuilding_BB(coor[3],coor[4])
                if coor[0] == 2:
                    self.map.updateBuilding_BN(coor[3],coor[4])
                if coor[0] == 3:
                    self.map.updateBuilding_BA(coor[3],coor[4])

                # self.map.b = False   
        elif getRXQueue().empty() == False :
            coor = getRXQueue().get()
            if int(coor[4]) == 0 : 
                self.map.updateCoor(coor[0],coor[1],coor[2]) 
    
                
        self.camera.update()
        for e in self.entities: e.update()
        self.gui.update()
        self.map.update(self.screen, self.camera)
        self.chatbox = self.events.chatbox
        self.game_time.update()
        self.save_game.update()
        self.load_game.update()
        self.map.actual_age = self.gui.age_sup
        if self.map.actual_age:
            self.map.load_images(self.map.actual_age)
            self.gui.icon_images = self.gui.load_icon_images(2)
            self.gui.tiles = self.gui.create_build_gui()
        while self.map.events.pause:
            if not self.menu.pause:
                self.map.events.pause = False
            self.menu.display_pause()
        self.map.events.Save_game = self.menu.save

    def draw(self):
        self.screen.fill(BLACK)  # On dessine un background noir sur lequel on dessine tout le GUI et la map
        self.map.draw(self.screen, self.camera)
        self.gui.draw(self.screen)
        self.map.draw_mini(self.screen, self.camera)
        draw_text(
            self.screen,  # print it on screen
            "{} FPS".format(round(self.clock.get_fps())),  # get value
            FONT_SIZE,  # text's size
            WHITE,  # the text's colour
            (self.width * 0.005, self.height * 0.01)  # position of the text (x, y)
        )

        draw_text(
            self.screen,  # print it on screen
            f"%02d : %02d" % (self.game_time.minute, self.game_time.second),
            FONT_SIZE,  # text's size
            BLUE_SKY,  # the text's colour
            (self.width * 0.475, self.height * 0.01)  # position of the text (x, y)
        )

        pg.display.flip()

    def start_real_game(self):
        self.map.build_blue_camp(STARTING_POS1)
        self.map.build_red_camp(STARTING_POS2)
        self.real_game = True
