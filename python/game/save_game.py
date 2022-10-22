from settings import save_units, save_entities, save_map
from typing import DefaultDict
import json


# press SPACE to save game
class Save_game:
    def __init__(self, world):
        self.world = world

    # we can use this function to save and load game :)))
    def scan_map(self):
        carte = DefaultDict(list)
        for x in range(self.world.grid_size_x):
            for y in range(self.world.grid_size_y):
                if (self.world.world[x][y]["tile"] == ""):
                    continue
                carte['%02d,%02d' % (x, y)] = self.world.world[x][y]["tile"]
        # Serializing json 
        json_object = json.dumps(carte, indent=4)
        # Writing to sample.json
        with open(save_map, "w") as outfile:
            outfile.write(json_object)

    def scan_units(self):
        units = DefaultDict(list)
        eleAttr = []  # team, pos, health, name, target_pos
        temp_key = 0
        for x in range(self.world.grid_size_x):
            for y in range(self.world.grid_size_y):
                if (self.world.units[x][y] is None):
                    continue
                eleAttr.append(self.world.units[x][y].team)
                eleAttr.append(self.world.units[x][y].pos)
                eleAttr.append(self.world.units[x][y].health)
                eleAttr.append(self.world.units[x][y].name)
                eleAttr.append(self.world.units[x][y].target)
                if self.world.units[x][y].name == "Villager":
                    eleAttr.append(self.world.units[x][y].in_work)
                units[str(temp_key)] = eleAttr
                eleAttr = []
                temp_key += 1

        # Serializing json 
        json_object = json.dumps(units, indent=4)
        # Writing to sample.json
        with open(save_units, "w") as outfile:
            outfile.write(json_object)

    def scan_entities(self):
        entities = DefaultDict(list)
        eleAttr = []  # team, pos, health, name
        temp_key = 0
        for element in self.world.entities:
            eleAttr.append(element.team)
            eleAttr.append(element.pos)
            eleAttr.append(element.health)
            eleAttr.append(element.name)
            eleAttr.append(element.age)
            entities[str(temp_key)] = eleAttr
            temp_key += 1
            eleAttr = []
        # Serializing json 
        json_object = json.dumps(entities, indent=4)
        # Writing to sample.json
        with open(save_entities, "w") as outfile:
            outfile.write(json_object)

    def update(self):
        if self.world.events.update_save_game():
            # press SPACE to save game
            self.scan_map()
            self.scan_entities()
            self.scan_units()
            # print(' save ')

        else:
            pass
            # print('save nothing')


class Load_game:
    def __init__(self, world):
        self.world = world
        f_entities = open(save_entities)
        f_map = open(save_map)
        f_units = open(save_units)
        self.load_map = json.load(f_map)
        self.load_units = json.load(f_units)
        self.load_entities = json.load(f_entities)
        self.loaded = False

    def load_game(self):
        pass

    def update(self):
        if self.world.events.Load_game and not self.loaded:
            self.world.reconstruct()
            self.loaded = True

        self.world.events.update_load_game()

    def get_buildings(self):
        # buildings = [[None for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        # for i in self.load_entities.keys():
        #     entity = self.load_entities[i]
        #     ent = None
        #     if entity[3] == "TownCenter":
        #         ent = TownCenter(entity[2], self.resource_manager, entity[0], False)    # false is the age of this building
        #     buildings[entity[2][0]][entity[2][1]] = ent

        return self.load_entities

        # if self.gui.selected_tile["name"] == "TownCenter":
        #     ent = TownCenter(render_pos, self.resource_manager, "Blue", False)
        #     self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
        #     self.buildings[grid_pos[0]][grid_pos[1]] = ent

    def get_units(self):
        return self.load_units

    def get_map(self):
        return self.load_map
