import pygame as pg
from settings import *
from game.resource import *
from game.map import *
from os import path


# from units import *

class Building:
    def __init__(self, pos, resource_man, team, beginning):
        # self.rect = self.image.get_rect(topleft=pos)
        self.resource_man = resource_man
        self.health_bar_length = HEALTH_BAR_LENGTH_BUILDING
        self.health_ratio = self.health_max / self.health_bar_length
        self.team = team
        self.pos = pos
        self.age_2 = False
        self.age = 'Firstage'
        self.attack_cooldown = pg.time.get_ticks()
        self.constructed = False
        if not beginning:
            self.resource_man.buy(self)

    def update(self):
        if not self.constructed:
            if self.health < self.health_max:
                self.health += 10
                if self.health >= self.health_max:
                    self.constructed = True
        if self.age_2:
            self.constructed = False

    def health_bar(self):
        for i in range(4):
            # pg.draw.rect(sprite, BLACK, (1+i, 1+i,entity.health_bar_length, 5), 4)
            pg.draw.rect(self.bar_image, BLACK, (-i, -i, self.health_bar_length, 5), 5)

        pg.draw.rect(self.bar_image, GREEN, (1, 1, (self.health / self.health_ratio) - 9, 5))
        return self.bar_image

    def passer_age(self):
        if self.game_name == 'Forum':
            print('je suis là')
            self.age = 'Secondage'
            if self.resource_man.buy_age(self) != -1 and self.age_2:
                self.bar_image = self.secondage_image.copy()
                self.image = self.secondage_image
                self.age_2 = False
                print("et ici")
                self.health_max += 1000
                if self.health == self.health_max:
                    self.health += 1000
                self.health_ratio = self.health_max / self.health_bar_length
            elif self.team == 'Red':
                self.bar_image = self.secondage_image.copy()
                self.image = self.secondage_image
                self.age_2 = False
                self.health_max += 1000
                if self.health == self.health_max:
                    self.health += 1000
                self.health_ratio = self.health_max / self.health_bar_length

            else:
                self.age = 'Firstage'
        else:
            self.age = 'Secondage'
            if self.age_2:
                self.bar_image = self.secondage_image.copy()
                self.image = self.secondage_image
                self.age_2 = False
                self.health_max += 1000
                if self.health == self.health_max:
                    self.health += 1000
                self.health_ratio = self.health_max / self.health_bar_length


class TownCenter(Building):
    bar_image = firstage_towncenter.copy()
    image = firstage_towncenter
    secondage_image = secondage_towncenter
    name = "TownCenter"
    game_name = "Forum"
    health = 0
    health_max = 1000


class Barracks(Building):
    bar_image = firstage_barracks.copy()
    image = firstage_barracks
    secondage_image = secondage_barracks
    name = "Barracks"
    game_name = "Caserne"
    health = 0
    health_max = 500


class Archery(Building):
    bar_image = firstage_archery.copy()
    image = firstage_archery
    secondage_image = secondage_archery
    name = "Archery"
    game_name = "Camp de tir à l'arc"
    health = 0
    health_max = 500


class Stable(Building):
    bar_image = stable.copy()
    image = stable
    secondage_image = stable
    name = "Stable"
    game_name = "Ecurie"
    health = 0
    health_max = 500
