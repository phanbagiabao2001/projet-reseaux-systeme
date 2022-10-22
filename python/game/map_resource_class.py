import pygame as pg
from settings import *
from game.map import *
from os import path


class MapResource:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.resource_cooldown = pg.time.get_ticks()
        self.available = True

    def mine(self, team=""):
        if self.the_rest > 0 and self.available:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                if team == "Blue":
                    self.the_rest -= 1
                    self.resource_cooldown = now
                    self.resource_manager.starting_resources[self.resource_type] += 1
                elif team == "Red":
                    self.the_rest -= 1
                    self.resource_cooldown = now
                    self.resource_manager.starting_resources_AI[self.resource_type] += 1
                else:
                    pass

            return 1
        else:
            self.available = False

    def get_rest(self):
        return self.the_rest


class Map_Tree(MapResource):
    game_name = "Arbre"
    image = Tree_img
    the_rest = 100
    the_rest_max = 100
    resource_type = "Wood"


class Map_Rock(MapResource):
    game_name = "Carrière de pierre"
    image = Rock_img
    the_rest = 350
    the_rest_max = 350
    resource_type = "Rock"


class Map_Gold(MapResource):
    game_name = "Or"
    image = Gold_img
    the_rest = 800
    the_rest_max = 800
    resource_type = "Gold"


class Map_Bush(MapResource):
    game_name = "Buisson"
    image = Bush_img
    the_rest = 150
    the_rest_max = 150
    resource_type = "Food"


class Map_Tile:
    def __init__(self):
        self.the_rest = 0

    def _____(self):
        pass

    def get_rest(self):
        return self.the_rest
