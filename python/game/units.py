import time
import pygame as pg
from settings import *
from os import path
# from units import *
from game.resource import *
# from tqdm import tqdm

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from connection import wrapper
from share_data import getTXQueue

class Unit:

    def __init__(self, tile, map, resource_man, team, beginning,id = -1):
        self.map = map
        self.tile = tile
        self.team = team  # blue team is the player's team
        self.alive = True
        self.resource_man = resource_man
        if not beginning:
            self.resource_man.buy(self)

        self.health_bar_length = HEALTH_BAR_LENGTH_UNIT
        self.health_ratio = self.health_max / self.health_bar_length

        self.map.units[tile["grid"][0]][tile["grid"][1]] = self             # it's too late, but if we replace tile["grid"][1] by tile["grid"][1] - 1, it'll be better

        self.pos = (tile["grid"][0], tile["grid"][1])

        self.map.list_troop.append(self)
        self.path_index = 0
        self.move_timer = pg.time.get_ticks()
        self.attack_cooldown = pg.time.get_ticks()

        self.target = None

        self.previous_time = 0
        self.id = id
    def get_health(self, type):
        if type == 'current':
            return self.health
        elif type == 'max':
            return self.health_max

    def die(self):
        self.alive = False
        index = self.map.list_troop.index(self)
        self.map.list_troop.pop(index)
        self.map.gui.examined_unit = None
        self.map.examine_unit = None

    def change_tile(self, pos):
        x = pos[0]
        y = pos[1]
        self.map.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        if self.map.units[x][y] is None:
            self.map.units[x][y] = self
            self.tile = self.map.world[x][y]
            return True
        # else:
        #     self.world.units[x][y+1] = self
        #     self.tile = self.world.world[x][y+1]
        #     return False

    def kill(self, cible):
        now = pg.time.get_ticks()
        if now - self.attack_cooldown > 2000:
            if cible.health <= 0:
                cible.health = 0
                print(cible, "meurt")
                self.attack_cooldown = now
            else:
                cible.health -= self.attack
                self.attack_cooldown = now

    def create_path(self, pos):
        searching_for_path = True
        while searching_for_path:
            x = pos[0]
            if pos[1] == 0:
                y = 0
            else:
                y = pos[1] - 1
            if (self.map.world[x][y]["collision"]):
                return
            if (self.map.units[x][y] is not None):
                return
            dest_tile = self.map.world[x][y]

            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.map.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x, y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False

    def set_target(self, pos):
        self.target = pos
        print("...." + str(self.target))
        getTXQueue().put([float(self.target[0]),float(self.target[1]),self.id,0,0])
    def update(self):
        temps_temp = pg.time.get_ticks()
        temps = temps_temp - self.previous_time
        if temps > self.velocity_inverse:
            if self.target is not None:
                self.create_path(self.target)
                try:
                    try:
                        if (self.path == []):
                            self.path.append([self.tile["grid"][0], self.tile["grid"][1]])
                        if [self.tile["grid"][0], self.tile["grid"][1]] == self.path[-1]:
                            self.target = None
                    except IndexError:
                        print(self.path)
                        print("------")
                        print(self.tile["grid"])
                    else:
                        if len(self.path) > 1:
                            new_pos = self.path[1]
                            self.pos = new_pos
                            if (not self.change_tile(new_pos)):
                                new_pos = self.path[2]
                                self.change_tile(new_pos)

                except AttributeError:
                    pass
        if temps > self.velocity_inverse:
            self.previous_time = temps_temp

    def health_bar(self):
        for i in range(4):
            pg.draw.rect(self.bar_image, BLACK, (-i, -i, self.health_bar_length, 5), 5)

        pg.draw.rect(self.bar_image, GREEN, (1, 1, (self.health / self.health_ratio) - 9, 5))
        return self.bar_image

    def get_attack_range(self):
        x,y = self.pos
        list_posible_range = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                list_posible_range.append((i,j))
        list_posible_range.remove((x,y))
        return list_posible_range



class Archer(Unit):
    bar_image = archer.copy()
    image = archer
    name = "Archer"
    game_name = "Archer"
    health = 50
    health_max = 50
    attack = 5
    range = 6
    velocity_inverse = 100


class Villager(Unit):
    bar_image = villager.copy()
    image = villager
    name = "Villager"
    game_name = "Villageois"
    health = 30
    health_max = 30
    attack = 3
    range = 4
    velocity_inverse = 200
    in_work = False


class Infantryman(Unit):
    bar_image = infantryman.copy()
    image = infantryman
    name = "Infantryman"
    game_name = "Barbare"
    health = 70
    health_max = 70
    attack = 7
    range = 1
    velocity_inverse = 300


class Cavalier(Unit):
    bar_image = cavalier.copy()
    image = cavalier
    name = "Cavalier"
    game_name = "Cavalier"
    health = 125
    health_max = 125
    attack = 8
    range = 1
    velocity_inverse = 65

class Bigdaddy(Unit):
    bar_image = supra.copy()
    image = supra
    name = "Bigdaddy"
    game_name = "Bigdaddy"
    health = 500
    health_max = 500
    attack = 600
    range = 15
    velocity_inverse = 25
