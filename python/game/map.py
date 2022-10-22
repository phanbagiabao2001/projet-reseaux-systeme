import pygame as pg
from share_data import getRXQueue, getTXQueue, getRBQueue
from settings import *
import random
import noise
from os import path
from .buildings import TownCenter, Barracks, Archery, Stable
from .units import Archer, Infantryman, Villager, Cavalier, Bigdaddy
from .events import *
from .map_resource_class import Map_Tree, Map_Tile, Map_Bush, Map_Gold, Map_Rock, MapResource
from connection import wrapper


# FOG_BLACK = -1
# FOG_GREY = 0
# FOG_NONE = 1

class Map:

    # create the dimensions of the world (isometric)
    def __init__(self, resource_man, entities, gui, grid_size_x, grid_size_y, width, height, events,b = 0):

        self.resource_man = resource_man
        self.entities = entities
        self.gui = gui
        self.grid_size_x = grid_size_x  # number of square in x-dimension
        self.grid_size_y = grid_size_y  # number of square in y-dimension
        self.width = width
        self.height = height

        self.starting_resources = STARTING_RESOURCES

        self.perlin_scale = self.grid_size_x / 2
        self.octave = random.randint(1, 20)
        self.modifier = random.randint(80, 120)
        self.random_noise = random.randint(1, 2)

        self.choosing_pos_x = None
        self.choosing_pos_y = None

        self.pause = False

        self.grass_tiles = pg.Surface(
            (grid_size_x * TILE_SIZE * 2, grid_size_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        # convert_alpha():   change the pixel format of an image including per pixel alphas convert_alpha(Surface) -> Surface convert_alpha() -> Surface
        #                   Creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format
        #                   with per pixel alpha. If no surface is given, the new surface will be optimized for blitting to the current display.
        self.events = events
        self.actual_age = self.events.get_age_sup()
        self.tiles = self.load_images(False)
        self.fog = [[FOG_BLACK for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        self.world = self.build_world()
        self.collision_matrix = self.create_collision_matrix()
        self.changed_tiles = []

        self.buildings = [[None for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        self.units = [[None for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        self.blue_team_ent = []
        self.red_team_ent = []
        self.age_2_blue = []
        self.age_2_red = []

        self.temp_tile = None
        self.examine_tile = None
        self.examine_unit = None
        self.examine_target_unit = None

        # choose Arbre, rock or gold
        self.choose = None

        # self.moving_to_resource = False
        self.mining = False
        self.mined = None
        self.mining_position = None
        self.past_mining_pos = None

        self.list_mining = []

        self.list_troop = []

        self.attacking = False
        self.attacking_unit = False

        self.list_attacker_defender = []
        self.list_units_atk = []

        self.replace_water()

        self.load_game = None
        self.b = b
    def updateCoor(self,x,y,id):
            for unit in self.list_troop:
                if unit.id == id :
                    unit.target = (int(x),int(y))
                #unit.update()

    def updateBuilding_BB(self,x,y):
        ent = Barracks(self.world[int(x)][int(y)].get("render_pos"), self.resource_man, "Blue", False)
        self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
        self.buildings[int(x)][int(y)] = ent 
    
    def updateBuilding_BN(self,x,y):
        ent = TownCenter(self.world[int(x)][int(y)].get("render_pos"), self.resource_man, "Blue", False)
        self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
        self.buildings[int(x)][int(y)] = ent 
    # Archery
    def updateBuilding_BA(self,x,y):
        ent = Archery(self.world[int(x)][int(y)].get("render_pos"), self.resource_man, "Blue", False)
        self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
        self.buildings[int(x)][int(y)] = ent 
    # work in map
    def update(self, screen, camera):

        self.gui.events.update_bigdaddy()
        self.bigdaddy = self.gui.events.bigdaddy

        for uni in self.list_troop:
            if uni.health <= 0:
                self.units[uni.pos[0]][uni.pos[1]] = None
                if uni in self.list_troop:
                    self.list_troop.remove(uni)
                    del uni

        self.pause = self.events.pause

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        for ent in self.entities:

            if ent.team == 'Blue' and (ent not in self.blue_team_ent):
                self.blue_team_ent.append(ent)

            if ent.team == 'Red' and (ent not in self.red_team_ent):
                self.red_team_ent.append(ent)

            if ent.age_2 and (ent not in self.age_2_blue):
                self.age_2_blue.append(ent)

            if ent.age_2 and (ent not in self.age_2_red):
                self.age_2_red.append(ent)

        if self.age_2_blue != []:
            for building in self.blue_team_ent:
                building.passer_age()
            self.events.remise_age()
        if self.age_2_red != []:
            for building in self.red_team_ent:
                building.passer_age()
            self.events.remise_age()

        if mouse_action[2]:
            self.examine_tile = None
            self.gui.examined_tile = None
            self.choose = None

        if mouse_action[0]:
            self.examine_unit = None
            self.gui.examined_unit = None

        self.temp_tile = None

        # je vais creer une fonction pour garder cette if-else condition
        if self.gui.selecting_building is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            # print(f"grid_pos(0): {grid_pos[0]}  grid_pos(1): {grid_pos[1]}")
            # on placer gui ici
            if self.allowed_tile(grid_pos):

                # print('placer gui')
                img = self.gui.selecting_building["image"].copy()
                img.set_alpha(100)

                # this if is to avoid the error: "index out of range" when your mouse run out of map
                if grid_pos[0] < self.grid_size_x and grid_pos[1] < self.grid_size_y:
                    render_pos = self.world[grid_pos[0]][grid_pos[1]].get("render_pos")
                    iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                    self.temp_tile = {
                        "image": img,
                        "render_pos": render_pos,
                        "iso_poly": iso_poly,
                        "collision": collision
                    }
                else:
                    pass

                # ce bloc de code sert à construire un bâtiment à un endroit où il n'y a pas de collision
                if mouse_action[0] and (not collision):
                    grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                    building = self.buildings[grid_pos[0]][grid_pos[1]]
                    if building is None:
                        if self.gui.selecting_building["name"] == "TownCenter":
                            ent = TownCenter(render_pos, self.resource_man, "Blue", False)
                            self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # getTXQueue().put([float(grid_pos[0]),float(grid_pos[1]),0,2])
                            # self.b = 1
                            getTXQueue().put([2,0,0,float(grid_pos[0]),float(grid_pos[1])])

                        
                        elif self.gui.selecting_building["name"] == "Barracks":
                            ent = Barracks(render_pos, self.resource_man, "Blue", False)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            # coor = getTXQueue().get()
                            
                            getTXQueue().put([1,0,0,float(grid_pos[0]),float(grid_pos[1])])
                            

                            # wrapper.send_peer(grid_pos[0],grid_pos[1],0,0)
                        elif self.gui.selecting_building["name"] == "Archery":
                            ent = Archery(render_pos, self.resource_man, "Blue", False)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                            getTXQueue().put([3,0,0,float(grid_pos[0]),float(grid_pos[1])])

                        elif self.gui.selecting_building["name"] == "Stable":
                            ent = Stable(render_pos, self.resource_man, "Blue", False)
                            self.entities.append(ent)
                            self.buildings[grid_pos[0]][grid_pos[1]] = ent
                        # if self.b == True:
                        #     # coor = getRBQueue().get()
                        #     ent = Barracks(render_pos, self.resource_man, "Blue", False)
                        #     self.entities.append(ent)
                        #     self.buildings[int(self.list_pos[2])][int(self.list_pos[3])] = ent
                        #     self.b = False
                        self.collision_matrix[grid_pos[1]][grid_pos[0]] = 0
                        self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                        self.gui.selecting_building = None
                    else:
                        pg.draw.polygon(screen, RED, iso_poly, 3)


        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if self.allowed_tile(grid_pos):  # and wood > resource:
                if grid_pos[0] < self.grid_size_x and grid_pos[1] < self.grid_size_y:
                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                    building = self.buildings[grid_pos[0]][grid_pos[1]]
                    if grid_pos[1] > 0:
                        units = self.units[grid_pos[0]][grid_pos[1] - 1]
                    else:
                        units = self.units[grid_pos[0]][grid_pos[1]]

                    if mouse_action[0] and (
                            building is not None):  # Si on a selectionné un bâtiment avec le clic gauche on affiche
                        self.examine_tile = grid_pos
                        self.gui.examined_tile = building

                    # si on clic gauche sur aucun bâtiment on n'affiche plus son GUI
                    if mouse_action[0] and (building is None):
                        self.choosing_pos_x = None
                        self.choosing_pos_y = None
                        self.examine_tile = None
                        self.gui.examined_tile = None

                    if mouse_action[0] and (units is not None) and (
                            self.examine_unit is None):  # Si on a selectionné une troupe avec le clic gauche on affiche
                        self.examine_unit = grid_pos
                        self.gui.examined_unit = units


                    if mouse_action[
                        0] and collision:  # Si on a selectionné une ressource avec le clic gauche on affiche
                        self.choose = grid_pos
                        self.gui.mining_gui = False
                        self.gui.choose = self.world[grid_pos[0]][grid_pos[1]]

                    if mouse_action[
                        0] and not collision:  # Si on clic gauche dans le vide on ferme tous les interfaces de sélection
                        self.choose = None
                        self.gui.choose = None

                    if mouse_action[2] and collision and (self.gui.examined_unit is not None):  # Si on a sélectionné
                        # une troupe et qu'on clic droit quelque part sur une ressource
                        self.choose = grid_pos  # on choisit la ressource correspondante
                        self.gui.choose = self.world[grid_pos[0]][grid_pos[1]]
                        # self.mining = True  # on active le mode minage
                        self.gui.mining_gui = True  # et on active le gui de minage

                    if self.gui.events.bigdaddy:
                        self.bigdaddy_spawn()



                    if self.gui.events.get_troop() is not None:
                        if (self.examine_tile and self.gui.examined_tile) is not None:
                            pos = self.examine_tile
                            pos_x = pos[0]
                            pos_y = pos[1]
                            # ce bloc est la réponse de l'appel de la fonction create_troop dans events en créant la
                            # troupe concernée
                            if self.gui.events.get_troop() == "archer" and self.resource_man.is_affordable(
                                    "Archer"
                            ):
                                a = Archer(
                                    self.world[pos_x][pos_y], # position actuelle du bâtiment créant l'unité
                                    self, # le monde actuel
                                    self.resource_man, # instancie la classe ressource qui va "payer" l'unité
                                    self.gui.examined_tile.team, # l'équipe du bâtiment qui crée l'unité
                                    False, # indiquer que ce n'est pas le début de la partie, l'unité côute
                                            # alors des ressources
                                )
                                self.list_troop.append(a) # ajout de l'unité dans la liste d'unités
                                self.examine_tile = None
                                self.gui.events.remise_troop() # pour éviter qu'on crée en boucle des unités

                            elif (
                                    self.gui.events.get_troop() == "infantryman"
                                    and self.resource_man.is_affordable("Infantryman")
                            ):
                                i = Infantryman(
                                    self.world[pos_x][pos_y],
                                    self,
                                    self.resource_man,
                                    self.gui.examined_tile.team,
                                    False,
                                )
                                self.list_troop.append(i)
                                self.examine_tile = None
                                self.gui.events.remise_troop()

                            elif self.gui.events.get_troop() == "villager" and self.resource_man.is_affordable(
                                    "Villager"
                            ):
                                v = Villager(
                                    self.world[pos_x][pos_y],
                                    self,
                                    self.resource_man,
                                    self.gui.examined_tile.team,
                                    False,
                                )
                                self.list_troop.append(v)
                                self.examine_tile = None
                                self.gui.events.remise_troop()

                            elif self.gui.events.get_troop() == "cavalier" and self.resource_man.is_affordable(
                                    "Cavalier"
                            ):
                                v = Cavalier(
                                    self.world[pos_x][pos_y],
                                    self,
                                    self.resource_man,
                                    self.gui.examined_tile.team,
                                    False,
                                )
                                self.list_troop.append(v)
                                self.examine_tile = None
                                self.gui.events.remise_troop()

                        self.gui.events.remise_troop()

                    if self.events.get_grid_pos_unit():
                        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                        building = self.buildings[grid_pos[0]][grid_pos[1]]
                        target_unit = self.units[grid_pos[0]][grid_pos[1] - 1]
                        if (self.gui.examined_unit is not None) and (self.gui.examined_unit.team == "Blue"):
                            new_unit_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                            new_unit_pos_world = self.grid_to_world(new_unit_pos[0], new_unit_pos[1])
                            # si on clic droit autre part que sur une ressource:
                            if target_unit is not None and (
                                    target_unit.team == "Red"):  # Si on a selectionné une troupe avec le clic gauche on affiche
                                atk_range = self.gui.examined_unit.get_attack_range()
                                couple_u = (self.gui.examined_unit, target_unit)
                                if (target_unit.pos in atk_range):
                                    self.attacking_unit = True
                                    if couple_u not in self.list_units_atk:
                                        self.list_units_atk.append(couple_u)
                            if not collision:  # and new_unit_pos_world["collision"])
                                couple = (self.gui.examined_unit, building)
                                # self.gui.examined_unit.change_tile(new_unit_pos)
                                if building is not None and (building.team == 'Red'):

                                    self.attacking = True
                                    if couple not in self.list_attacker_defender:
                                        self.list_attacker_defender.append((self.gui.examined_unit, building))

                                elif mouse_action[2] and (building is None):
                                    self.gui.examined_unit.set_target((new_unit_pos[0], new_unit_pos[1]))
                                    self.mining_position = None
                                    self.attacking = False
                                    self.mining = False
                                    self.examine_unit = new_unit_pos
                                    self.events.remise_moving_troop()


                            # si on clic droit sur une ressource pour la miner avec un villageois:
                            elif self.gui.examined_unit.name == "Villager" and collision:
                                self.attacking = False
                                # self.gui.examined_unit.change_tile((new_unit_pos[0]+1,new_unit_pos[1]))
                                new_unit_pos = (new_unit_pos[0] + 1, new_unit_pos[1])
                                self.gui.examined_unit.set_target(new_unit_pos)
                                # print("mining", self.gui.examined_unit.name, "to", new_unit_pos)
                                self.events.remise_moving_troop()
                                # on vérifie qu'on a bien sélectionné une ressource
                                if self.gui.choose is not None:
                                    # et qu'elle dispose toujours de ressources
                                    if self.gui.choose["class"].available:
                                        self.mining = True
                                        # condition permettant de changer de ressource minée sans que la précédente soit toujours minée
                                        if new_unit_pos != self.mining_position and (self.mining_position is not None):
                                            self.list_mining.remove(self.mined)
                                        self.mined = self.gui.choose
                                        self.mined["mining_team"] = "Blue"
                                        self.events.getting_resource()
                                        # self.moving_to_resource = True
                                        self.mining_position = self.gui.choose
                                        # print("mining pos:", self.mining_position)
                                        self.list_mining.append(self.mined)

                                    elif not self.gui.choose["class"].available:
                                        # self.moving_to_resource = False
                                        self.mining = False
                                        self.events.getting_resource()
                                        # condition permettant de vider la variable contenant l'objet ressource miné précédemment (peut être None)
                                        if self.mined in self.list_mining:
                                            self.list_mining.remove(self.mined)
                                        self.mined = None
                                        self.choose = None
                                        self.gui.choose = None
                                        self.mining_position = None
                                        self.gui.mining_gui = False

                    # if self.mining and self.moving_to_resource and self.events.getting_resource:
                    #     self.mined["class"].mine()

                    if self.mining and self.events.getting_resource:
                        for mined in self.list_mining:
                            mined["class"].mine(mined["mining_team"])
                            # pass
                            # on mine la ressource tant que self.mining = True

                    if self.attacking:
                        # ad est un tuple avec (attaquant, défenseur)
                        # pour tous les tuples ad, on réalise des attaques avec la boucle for
                        for ad in range(len(self.list_attacker_defender)):
                            couple = self.list_attacker_defender[ad]
                            if couple[1].health <= 0:  # on supprime le bâtiment
                                bat_pos = couple[1].pos
                                self.world[bat_pos[0]][bat_pos[1]]["collision"] = False
                                index = self.entities.index(couple[1])
                                self.examine_tile = None
                                self.gui.examined_tile = None
                                self.entities.pop(index)
                                self.buildings[bat_pos[0]][bat_pos[1]] = None
                                self.choosing_pos_x, self.choosing_pos_y = None, None
                                self.attacking = False
                                ind = self.list_attacker_defender.index(couple)
                                self.list_attacker_defender.pop(ind)

                            else:
                                couple[0].kill(couple[1])

                    if self.attacking_unit:
                        for ad in self.list_units_atk:
                            if (ad[0].health ==0 or ad[1].health == 0):
                                self.list_units_atk.pop(self.list_units_atk.index(ad))
                            atk_rg = ad[0].get_attack_range()
                            if ad[1].pos in atk_rg:
                                ad[0].kill(ad[1])              
                            else:
                                self.list_units_atk.pop(self.list_units_atk.index(ad))

                    if self.events.update_destroy():
                        # condition qui récupère la variable dans events permettant de savoir si on veut détruire
                        # en gros on supprimer toute trace du bâtiment et on enlève le GUI de ce dernier
                        if self.choosing_pos_x is not None and (self.choosing_pos_y is not None):
                            building = self.buildings[self.choosing_pos_x][self.choosing_pos_y]
                            if building is not None:
                                self.world[self.choosing_pos_x][self.choosing_pos_y]["collision"] = False
                                index = self.entities.index(building)
                                self.examine_tile = None
                                self.gui.examined_tile = None
                                # print(index)
                                self.entities.pop(index)
                                self.buildings[self.choosing_pos_x][self.choosing_pos_y] = None
                                self.events.remise()
                                self.choosing_pos_x, self.choosing_pos_y = None, None

        for unit in self.list_troop:
            # unit.health_bar()
            if unit.target is not None:
                unit.update()

    # quand le prog est grandi on doit update plusieurs choses comme heal, shield ou attack point ici
    def draw_mini(self, screen, camera):

        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                render_pos = self.world[x][y]["render_pos"]
                tile = self.world[x][y]["tile"]
                # minimap here
                minimap_offset = [50, self.height * 0.77 - 20]
                render_pos_mini = self.world[x][y]["render_pos_mini"]
                if tile == "Arbre":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, GREEN, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)
                elif tile == "Carrière de pierre":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, VIOLET, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)
                elif tile == "Or":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, YELLOW_LIGHT, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)

                elif tile == "Buisson":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, PINK, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)

                elif tile == "Eau":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, BLUE_SKY, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)

                elif self.units[x][y] is not None:
                    # render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7
                    pg.draw.circle(screen, self.units[x][y].team, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   2)
                elif self.buildings[x][y] is not None:
                    pg.draw.circle(screen, self.buildings[x][y].team, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   2)
                mini = self.world[x][y]["iso_poly_mini"]
                mini = [(x + 200 + minimap_offset[0], y + 20 + minimap_offset[1]) for x, y in
                        mini]  # position x + ...., y  + ...
                pg.draw.polygon(screen, MINI_MAP_COLOUR, mini, 1)

    def get_grid_array(self):
        grid = []
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                grid.append(self.world[x][y]["grid"])

        return grid

    def is_neighbor(self, ind1, ind2):
        if ind1[0] == ind2[0]:
            return True if ind1[1] == ind2[1] + 1 or ind1[1] == ind2[1] - 1 else False
        elif ind1[1] == ind2[1]:
            return True if ind1[0] == ind2[0] + 1 or ind1[0] == ind2[0] - 1 else False
        else:
            return False

    def neighbor_list(self, list, grid):
        neighbors = []
        neighbors.append((grid[0], grid[1] + 1))
        return neighbors

    def replace_water(self):
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                tile = self.world[x][y]["tile"]
                if tile == 'Eau' and not (self.world[x][y] in self.changed_tiles):
                    neighbors = self.neighbor_list(self.get_grid_array(), self.world[x][y]["grid"])
                    for i in range(len(neighbors)):
                        checking_tile = self.grid_to_world(neighbors[i][0], neighbors[i][1])
                        if checking_tile["tile"] == "Eau":
                            pass
                        else:
                            self.changed_tiles.append(self.world[x][y])

        for changing_tiles in self.changed_tiles:
            changing_tiles["tile"] = ''

    def mark_fog_to_none(self, unit_x, unit_y, check_team):
         d = 2
         for x in range(self.grid_size_x):
             for y in range(self.grid_size_y):
                 if check_team == "Blue":
                     if ((x-unit_x)**2 + (y-unit_y)**2) < d**2 :
                         self.fog[x][y] = FOG_NONE

    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_size_x):
             for y in range(self.grid_size_y):
                 if self.fog[x][y] == FOG_NONE:
                     self.fog[x][y] = FOG_GREY

        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                render_pos = self.world[x][y]["render_pos"]
                # conditions pour surligner les objets qu'on sélectionne afin de mieux les voir
                tile = self.world[x][y]["tile"]
                if tile != "" and self.world[x][y]["class"].available:
                    screen.blit(self.tiles[tile],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.choose is not None:
                        if (x == self.choose[0]) and (y == self.choose[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)

                units = self.units[x][y]
                if units is not None:
                    self.mark_fog_to_none(x,y,units.team)
                    screen.blit(units.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (units.image.get_height() - TILE_SIZE) + camera.scroll.y))

                    screen.blit(units.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (units.image.get_height() - TILE_SIZE) + camera.scroll.y))

                    if self.examine_unit == (x, y + 1) or (units.health < units.health_max):
                        screen.blit(units.health_bar(),
                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     render_pos[1] - (units.health_bar().get_height() - TILE_SIZE) + camera.scroll.y))

                    if self.examine_unit is not None:
                        if (x == self.examine_unit[0]) and (y == self.examine_unit[1] - 1):
                            mask = pg.mask.from_surface(units.image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (units.image.get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            pg.draw.polygon(screen, self.units[x][y].team, mask, 2)

                building = self.buildings[x][y]
                if building is not None:
                    self.mark_fog_to_none(x,y,building.team)
                    screen.blit(building.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))

                    screen.blit(building.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))

                    if self.examine_tile == (x, y) or (building.health < building.health_max):
                        screen.blit(building.health_bar(),
                                    (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     render_pos[1] - (
                                             building.health_bar().get_height() - TILE_SIZE) + camera.scroll.y))

                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            self.choosing_pos_x, self.choosing_pos_y = x, y
                            pg.draw.polygon(screen, self.buildings[x][y].team, mask, 2)

        if self.temp_tile is not None:
            mouse_pos = pg.mouse.get_pos()
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            building = self.buildings[grid_pos[0]][grid_pos[1]]
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"] or building is not None:
                pg.draw.polygon(screen, RED, iso_poly, 3)
            else:
                pg.draw.polygon(screen, WHITE, iso_poly, 3)

            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )
        if self.events.chatbox.fog:
            for x in range(self.grid_size_x):
                 for y in range(self.grid_size_y):
                     if self.fog[x][y] != FOG_NONE:
                         render_pos = self.world[x][y]["render_pos"]
                         x_pixel = render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x
                         y_pixel = render_pos[1] + camera.scroll.y
                         rect = (x_pixel, y_pixel, TILE_SIZE, TILE_SIZE)
                         color = (0, 0, 0, 160) if self.fog[x][y] == FOG_GREY else (0,0,0,255)
                         shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
                         pg.draw.rect(shape_surf, color, shape_surf.get_rect())
                         screen.blit(shape_surf, rect)

    # create worlds based on created dimensions
    def build_world(self):

        world = []

        for grid_x in range(self.grid_size_x):
            world.append([])
            for grid_y in range(self.grid_size_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"],
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

        return world

    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0
        return collision_matrix

    def grid_to_world(self, grid_x, grid_y):

        # create a square with four vertices and their dimensions
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        rect_mini_map = [
            (grid_x * TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        iso_poly_mini = [self.cart_to_iso(x, y) for x, y in rect_mini_map]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        minx_mini = min([x for x, y in iso_poly_mini])
        miny_mini = min([y for x, y in iso_poly_mini])

        r = range(1, 500)
        o = 5
        # Faire une forêt
        perlin = 100 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale, octaves=o)

        if perlin >= 25:
            tile = "Eau"
        elif perlin <= -12.5:
            tile = "Arbre"
        elif 6 < perlin < 8:
            tile = "Buisson"
        elif 16 < perlin < 18 :
            tile = "Or"
        elif 22 < perlin < 24 :
            tile = "Carrière de pierre"
        else:
            # Mettre des rochers OU des mines d'or aléatoirement à un taux de 0.8%
            if (grid_x, grid_y) == STARTING_POS1:
                tile = ''
            elif r == 4:
                r2 = random.randint(1, 1)
                if r2 == 1:
                    tile = "Or"
                elif r2 == 2:
                    tile = "Carrière de pierre"
            elif 5 == r :
                tile = "Buisson"
            # Un arbre isolé sera placé ici à un taux de 10%
            elif r == 50:
                tile = "Arbre"
            else:
                tile = ""
                # Ne rien mettre sur le block

        # We create the Arbre's object here
        if tile == "Arbre":
            map_resource = Map_Tree(self.resource_man)
        # We create the rock's object here
        elif tile == "Carrière de pierre":
            map_resource = Map_Rock(self.resource_man)
        # We create the gold's object here
        elif tile == "Or":
            map_resource = Map_Gold(self.resource_man)
        # We create the bush's object here
        elif tile == "Buisson":
            map_resource = Map_Bush(self.resource_man)
        elif tile == "Eau":
            map_resource = Map_Tree(self.resource_man)

        # Tile's Object
        else:
            map_resource = None

        mining_team = ""
        # this dict() store all kind of info of all elements in grid
        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,  # square map
            "cart_rect_mini_map": rect_mini_map,  # square mini map
            "iso_poly": iso_poly,  # iso_poly map
            "iso_poly_mini": iso_poly_mini,  # isopoly minimap
            "render_pos": [minx, miny],
            "render_pos_mini": [minx_mini, miny_mini],
            "tile": tile,
            "collision": False if tile == "" else True,
            "class": map_resource,
            "mining_team": mining_team
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y
        # transform to card (inverse of card_to_iso)
        card_y = (2 * world_y - world_x) / 2
        card_x = card_y + world_x
        # transform to grid coordinates
        grid_x = int(card_x // TILE_SIZE)
        grid_y = int(card_y // TILE_SIZE)
        return grid_x, grid_y

    # load our blocks into the game
    def load_images(self, age):
        block = Block_img.convert_alpha()
        Arbre = Tree_img.convert_alpha()
        rock = Rock_img.convert_alpha()
        gold = Gold_img.convert_alpha()  # C'est ici que l'on va lier les entités du jeu à des images (sauf pour les troupes)
        bush = Bush_img.convert_alpha()
        water = Water_img.convert_alpha()
        building1 = firstage_towncenter.convert_alpha() if not age else secondage_barracks.convert_alpha()
        building2 = firstage_barracks.convert_alpha() if not age else secondage_barracks.convert_alpha()
        building3 = firstage_archery.convert_alpha() if not age else secondage_barracks.convert_alpha()
        building4 = stable.convert_alpha()
        images = {
            "building1": building1,
            "building2": building2,
            "building3": building3,
            "building4": building4,
            "Arbre": Arbre,
            "Carrière de pierre": rock,
            "block": block,
            "Or": gold,
            "Buisson": bush,
            "Eau": water
        }
        return images

    # collision here
    def allowed_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.gui.resources_rect, self.gui.build_rect, self.gui.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_size_x) and (0 <= grid_pos[1] <= self.grid_size_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False

    def build_blue_camp(self, starting_pos):
        self.constructed = False
        if not (self.grid_to_world(starting_pos[0], starting_pos[1]))["collision"]:
            ent = TownCenter(starting_pos, self.resource_man, "Blue", True)
            self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
            self.buildings[starting_pos[0]][starting_pos[1]] = ent
            villager_list = self.neighbor_list(self.get_grid_array(), (starting_pos[0], starting_pos[1] - 1))
            for villager in villager_list:
                index = villager_list.index(villager)
                pos_villager = villager_list[index]
                v = Villager(self.grid_to_world(pos_villager[0], pos_villager[1]), self, self.resource_man,
                             "Blue", True,id = 1)
                v1 = Villager(self.grid_to_world(pos_villager[0] + 2, pos_villager[1]), self, self.resource_man,
                             "Blue", True,id = 2)
                v2 = Villager(self.grid_to_world(pos_villager[0] - 2, pos_villager[1]), self, self.resource_man,
                             "Blue", True,id = 3)
                self.list_troop.append(v)
                self.list_troop.append(v1)
                self.list_troop.append(v2)
            self.constructed = True
        else:
            neighbors = self.neighbor_list(self.get_grid_array(), starting_pos)
            for pos in neighbors:
                if not (self.constructed and (self.grid_to_world(pos[0], pos[1])["collision"])):
                    self.build_blue_camp(starting_pos)
                    self.constructed = True
            if not self.constructed:
                print("Le Forum n'a pas pu être construit")

    def build_red_camp(self, starting_pos):
        self.constructed = False
        if not (self.grid_to_world(starting_pos[0], starting_pos[1]))["collision"]:
            ent = TownCenter(starting_pos, self.resource_man, "Red", True)
            self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
            self.buildings[starting_pos[0]][starting_pos[1]] = ent
            villager_list = self.neighbor_list(self.get_grid_array(), (starting_pos[0], starting_pos[1] - 1))
            for villager in villager_list:
                index = villager_list.index(villager)
                pos_villager = villager_list[index]
                v = Villager(self.grid_to_world(pos_villager[0], pos_villager[1]), self, self.resource_man,
                             "Red", True,id = 4)
                v1 = Villager(self.grid_to_world(pos_villager[0] + 2, pos_villager[1]), self, self.resource_man,
                             "Red", True,id = 5)
                v2 = Villager(self.grid_to_world(pos_villager[0] - 2, pos_villager[1]), self, self.resource_man,
                             "Red", True,id = 6)
                self.list_troop.append(v)
                self.list_troop.append(v1)
                self.list_troop.append(v2)
            
            self.constructed = True
        else:
            neighbors = self.neighbor_list(self.get_grid_array(), starting_pos)
            for pos in neighbors:
                if not (self.constructed and (self.grid_to_world(pos[0], pos[1])["collision"])):
                    self.build_blue_camp(starting_pos)
                    self.constructed = True
            if not self.constructed:
                print("Le Forum n'a pas pu être construit")


    def bigdaddy_spawn(self):
        a = Bigdaddy(
            self.world[25][25],
            self,
            self.resource_man,
            "Blue",
            False,
        )
        self.list_troop.append(a)
        self.examine_tile = None

    def reconstruct(self):
        self.entities = []

        self.buildings = [[None for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        self.units = [[None for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]

        self.blue_team_ent = []
        self.red_team_ent = []

        self.age_2_blue = []
        self.age_2_red = []

        self.mining = False
        self.mined = None
        self.mining_position = None
        self.past_mining_pos = None

        self.list_mining = []

        self.list_troop = []
        self.attacking = False
        self.attacking_unit = False
        self.list_attacker_defender = []

        map_world = []

        self.replace_water()

        for i in self.load_game.load_entities.keys():
            entity = self.load_game.load_entities[i]
            if entity[3] == "TownCenter":
                ent = TownCenter(entity[1], self.resource_man, entity[0],
                                 False)  # false is the age of this building
                ent.team = entity[0]
                ent.health = entity[2]
                ent.age = entity[4] == "Firstage"
                self.entities.append(ent)
                self.buildings[entity[1][0]][entity[1][1]] = ent
            if entity[3] == "Barracks":
                ent = Barracks(entity[1], self.resource_man, entity[0], False)  # false is the age of this building
                ent.team = entity[0]
                ent.health = entity[2]
                ent.age = entity[4] == "Firstage"
                self.entities.append(ent)
                self.buildings[entity[1][0]][entity[1][1]] = ent
            if entity[3] == "Archery":
                ent = Archery(entity[1], self.resource_man, entity[0], False)  # false is the age of this building
                ent.team = entity[0]
                ent.health = entity[2]
                ent.age = entity[4] == "Firstage"
                self.entities.append(ent)
                self.buildings[entity[1][0]][entity[1][1]] = ent

        for i in self.load_game.load_units.keys():
            unit = self.load_game.load_units[i]
            if unit[3] == "Villager":
                un = Villager(self.world[unit[1][0]][unit[1][1]], self, self.resource_man,
                              unit[0], False)
                un.target = unit[4]
                un.health = unit[2]
                un.in_work = unit[5]
                self.list_troop.append(un)
            if unit[3] == "Infantryman":
                un = Infantryman(self.world[unit[1][0]][unit[1][1]], self, self.resource_man,
                                 unit[0], False)
                un.target = unit[4]
                un.health = unit[2]
                self.list_troop.append(un)
            if unit[3] == "Archer":
                un = Archer(self.world[unit[1][0]][unit[1][1]], self, self.resource_man,
                            unit[0], False)
                un.target = unit[4]
                un.health = unit[2]
                self.list_troop.append(un)
            if unit[3] == "Bigdaddy":
                un = Bigdaddy(self.world[unit[1][0]][unit[1][1]], self, self.resource_man,
                            unit[0], False)
                un.target = unit[4]
                un.health = unit[2]
                self.list_troop.append(un)

        for i in self.load_game.load_map.keys():
            tile = self.load_game.load_map[i]
            pos_s = i.split(',')
            pos = [0, 0]
            pos[0] = int(pos_s[0])
            pos[1] = int(pos_s[1])
            map_resource = None

            if tile == "Arbre":
                map_resource = Map_Tree(self.resource_man)
                collision = True

            elif tile == "Carrière de pierre":
                map_resource = Map_Rock(self.resource_man)
                collision = True

            elif tile == "Or":
                map_resource = Map_Gold(self.resource_man)
                collision = True

            elif tile == "Buisson":
                map_resource = Map_Bush(self.resource_man)
                collision = True

            elif tile == "Eau":
                map_resource = Map_Tree(self.resource_man)
                collision = True

            elif tile == "":
                map_resource = None
                collision = False

            self.world[pos[0]][pos[1]]["tile"] = tile
            self.world[pos[0]][pos[1]]["collision"] = collision
            self.world[pos[0]][pos[1]]["class"] = map_resource
            map_world.append([pos[0], pos[1]])

        for x in range(50):
            for y in range(50):
                if [x, y] not in map_world:
                    self.world[x][y]["tile"] = ""
                    self.world[x][y]["collision"] = False
                    self.world[x][y]["class"] = None
