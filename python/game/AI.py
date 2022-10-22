# from typing import DefaultDict

# from pygame.mixer import find_channel
# from .events import *
# from settings import *
# from .buildings import *
# from .units import *
# import json

# action_dict = {
#     "TownCenter": 0,
#     "Barracks": 1,
#     "Archery": 2,
#     "Archer": 3,
#     "Infantryman": 4,
#     "Villager": 5,
#     "get_resource": 6,
#     "next-age": 7,
#     "Stable": 8,
#     "Cavalier": 9,
#     "All-attack": 10
# }


# class AI:
#     def __init__(self, game_time, map, resource_man):
#         self.game_time = game_time
#         self.map = map
#         self.resource_man = resource_man
#         self.previous_time = 0
#         self.created_tc = False
#         self.created_bar = False
#         self.created_arc = False
#         self.AI_unit = []
#         self.AI_villager = []
#         self.AI_batiment = []
#         self.age = 1
#         with open(AI_action_JSONfile) as f:
#             self.data = json.load(f)
#         self.function_list = [self.AI_construct_Towncenter, self.AI_construct_Barracks, self.AI_construct_Archery,
#                               self.create_Archer, self.create_Infantryman, self.create_villager, self.get_resource, 
#                               self.next_age, self.AI_construct_Stable,self.create_Cavalier,self.all_attack]
#         self.towncenter = self.AI_construct_Towncenter(5, 10)

#         self.all_in = False

#     def read_file(self):
#         action_line = self.f.readline()
#         if (action_line == ''):
#             action_line = ' - -(0,0)'
#         action_line = action_line.rsplit("\n")
#         action = action_line[0].split("-")
#         li = action[2][1:-1].split(',')
#         li = (int(li[0]), int(li[1]))
#         action[2] = li
#         return action

#     def AI_construct_Towncenter(self, x, y):
#         # print(f'construct a Towncenter at ({x},{y})')
#         if not self.map.world[x][y]["collision"]:
#             ent = TownCenter((x, y), self.resource_man, "Red", True)
#             self.map.entities.append(ent)
#             self.AI_batiment.append(ent)
#             self.map.buildings[x][y] = ent
#             self.created_tc = True
#             return ent
#         else:
#             if (0 < y < 49):
#                 return self.AI_construct_Towncenter(x, y + 1)
#             elif (0 < x < 49):
#                 return self.AI_construct_Towncenter(x + 1, y)

#     def AI_construct_Barracks(self, x, y):
#         # print(f'construct a Barrack at ({x},{y})')
#         if not self.map.world[x][y]["collision"]:
#             ent = Barracks((x, y), self.resource_man, "Red", False)
#             self.map.entities.append(ent)
#             self.AI_batiment.append(ent)
#             self.map.buildings[x][y] = ent
#             self.created_bar = True
#         elif (not self.map.world[x][y+1]["collision"]) or (not self.map.world[x+1][y]["collision"]):
#             if not self.map.world[x][y+1]["collision"]:
#                 self.AI_construct_Barracks(x, y + 1)
#             elif not self.map.world[x+1][y]["collision"]:
#                 self.AI_construct_Barracks(x + 1, y)
#         else:
#             if not self.map.world[x][y+2]["collision"]:
#                 self.AI_construct_Barracks(x, y + 2)
#             else:
#                 self.AI_construct_Barracks(x + 2, y)

#     def AI_construct_Archery(self, x, y):
#         # print(f'construct an Archery at ({x},{y})')
#         if not self.map.world[x][y]["collision"]:
#             ent = Archery((x, y), self.resource_man, "Red", False)
#             self.map.entities.append(ent)
#             self.AI_batiment.append(ent)
#             self.map.buildings[x][y] = ent
#             self.created_arc = True
#         elif (not self.map.world[x][y+1]["collision"]) or (not self.map.world[x+1][y]["collision"]):
#             if not self.map.world[x][y+1]["collision"]:
#                 self.AI_construct_Archery(x, y + 1)
#             elif not self.map.world[x+1][y]["collision"]:
#                 self.AI_construct_Archery(x + 1, y)
#         else:
#             if not self.map.world[x][y+2]["collision"]:
#                 self.AI_construct_Archery(x, y + 2)
#             else:
#                 self.AI_construct_Archery(x + 2, y)


#     def AI_construct_Stable(self, x, y):
#         # print(f'construct an Archery at ({x},{y})')
#         if not self.map.world[x][y]["collision"]:
#             ent = Stable((x, y), self.resource_man, "Red", False)
#             self.map.entities.append(ent)
#             self.AI_batiment.append(ent)
#             self.map.buildings[x][y] = ent
#             self.created_arc = True
#         elif (not self.map.world[x][y+1]["collision"]) or (not self.map.world[x+1][y]["collision"]):
#             if not self.map.world[x][y+1]["collision"]:
#                 self.AI_construct_Stable(x, y + 1)
#             elif not self.map.world[x+1][y]["collision"]:
#                 self.AI_construct_Stable(x + 1, y)
#         else:
#             if not self.map.world[x][y+2]["collision"]:
#                 self.AI_construct_Stable(x, y + 2)
#             else:
#                 self.AI_construct_Stable(x + 2, y)

#     # ================================================================================================================================================================
#     # =============================================================       GETTING RESSOURCE      =====================================================================
#     # ================================================================================================================================================================

#     def find_resource(self):
#         vill_dict = DefaultDict(list)
#         vill_list = []  # wood,rock,gold
#         i = 0
#         for villager in self.AI_villager:
#             # print(type(villager))
#             # self.map.units[self.tile["grid"][0]][self.tile["grid"][1]]
#             # print(f'x:{villager.tile["grid"][0]} y:{villager.tile["grid"][1]}')
#             # print(self.get_distance(villager, "Arbre"))
#             # print(self.get_distance(villager, "Carrière de pierre"))
#             # print(self.get_distance(villager, "Or"))
#             vill_list.append(self.get_distance(villager, "Arbre"))
#             vill_list.append(self.get_distance(villager, "Carrière de pierre"))
#             vill_list.append(self.get_distance(villager, "Or"))
#             vill_list.append(self.get_distance(villager, "Buisson"))
#             vill_dict[str(i)] = vill_list
#             vill_list = []
#             i += 1
#         return vill_dict

#     def get_resource(self, resource):
#         dict_resource = self.find_resource()
#         if (dict_resource == {}): return

#         if (resource == "Arbre"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
#                 if (dict_resource[i][0][2] < min_dictance):
#                     min_dictance = dict_resource[i][0][2]
#                     villa_pos = (dict_resource[i][0][0], dict_resource[i][0][1], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Arbre 1")
#                 self.get_new_resource("Arbre", 1)
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Arbre 2")
#                 self.get_new_resource("Arbre", 2)
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Arbre 3")
#                 self.get_new_resource("Arbre", 3)
#                 # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#             else:
#                 self.AI_villager[int(villa_pos[2])].set_target(
#                     (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#                 self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
#                 self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#                 self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#                 self.map.events.getting_resource()
#                 self.map.mining = True

#         if (resource == "Carrière de pierre"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue
#                 if (dict_resource[i][1][2] < min_dictance):
#                     min_dictance = dict_resource[i][1][2]
#                     villa_pos = (dict_resource[i][1][0], dict_resource[i][1][1], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Pierre 1")
#                 self.get_new_resource("Carrière de pierre", 1)
#                 # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#                 # # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Pierre 2")
#                 self.get_new_resource("Carrière de pierre", 2)
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Pierre 3")
#                 self.get_new_resource("Carrière de pierre", 3)
#                 # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#                 # # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Pierre 4")
#                 self.get_new_resource("Carrière de pierre", 4)
#                 # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#             self.AI_villager[int(villa_pos[2])].set_target(
#                 (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#             self.AI_villager[int(villa_pos[2])].in_work = True
#             self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#             self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#             self.map.events.getting_resource()
#             self.map.mining = True

#         if (resource == "Or"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue
#                 if (dict_resource[i][2][2] < min_dictance):
#                     min_dictance = dict_resource[i][2][2]
#                     villa_pos = (dict_resource[i][2][0], dict_resource[i][2][1], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Or 1")
#                 self.get_new_resource("Or", 1)
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Or 2")
#                 self.get_new_resource("Or", 2)
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Or 3")
#                 self.get_new_resource("Or", 3)
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#                 # print("change Or 4")
#                 self.get_new_resource("Or", 4)
#                 # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
#             self.AI_villager[int(villa_pos[2])].set_target(
#                 (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#             self.AI_villager[int(villa_pos[2])].in_work = True
#             self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#             self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#             self.map.events.getting_resource()
#             self.map.mining = True

#         if (resource == "Buisson"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue
#                 if (dict_resource[i][3][2] < min_dictance):
#                     min_dictance = dict_resource[i][3][2]
#                     villa_pos = (dict_resource[i][3][0], dict_resource[i][3][1], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 self.get_new_resource("Buisson", 1)
#                 self.get_new_resource("Buisson", 2)
#                 self.get_new_resource("Buisson", 3)
#                 self.get_new_resource("Buisson", 4)
#             self.AI_villager[int(villa_pos[2])].set_target(
#                 (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#             self.AI_villager[int(villa_pos[2])].in_work = True
#             self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#             self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#             self.map.events.getting_resource()
#             self.map.mining = True

#     def get_distance(self, villager, type_resource):

#         distance_list = []
#         for x in range(self.map.grid_size_x):
#             for y in range(self.map.grid_size_y):
#                 if self.map.world[x][y]["tile"] == type_resource:
#                     l = ((villager.tile["grid"][0] - x) ** 2 + (villager.tile["grid"][1] - y) ** 2) ** (1 / 2)
#                     distance_list.append((x, y, l))
#         temp_list = []
#         for i in distance_list:
#             temp_list.append(i[2])  # the same pos index of distance_list
#         if (temp_list == []) : return []
#         dictance_min = min(temp_list)
#         return distance_list[temp_list.index(dictance_min)]

#     # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++GETTING_NEW_RESSOURCE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#     def get_new_distance(self, villager, type_resource):

#         distance_list = []
#         for x in range(self.map.grid_size_x):
#             for y in range(self.map.grid_size_y):
#                 if self.map.world[x][y]["tile"] == type_resource:
#                     l = ((villager.tile["grid"][0] - x) ** 2 + (villager.tile["grid"][1] - y) ** 2) ** (1 / 2)
#                     distance_list.append((l, x, y))  # we do it for comparing two tuple. I must show a sorted list
#         return sorted(distance_list)

#     def find_new_resource(self):
#         vill_dict = DefaultDict(list)
#         vill_list = []
#         i = 0
#         for villager in self.AI_villager:
#             vill_list.append(self.get_new_distance(villager, "Arbre"))
#             vill_list.append(self.get_new_distance(villager, "Carrière de pierre"))
#             vill_list.append(self.get_new_distance(villager, "Or"))
#             vill_list.append(self.get_new_distance(villager, "Buisson"))
#             vill_dict[str(i)] = vill_list
#             vill_list = []
#             i += 1
#         return vill_dict

#     def get_new_resource(self, resource, i_th_time):
#         dict_resource = self.find_new_resource()
#         if (dict_resource == {}): return
#         if (resource == "Arbre"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
#                 if (dict_resource[i][0][i_th_time][0] < min_dictance):
#                     min_dictance = dict_resource[i][0][i_th_time][0]
#                     villa_pos = (dict_resource[i][0][i_th_time][1], dict_resource[i][0][i_th_time][2], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 return
#             else:

#                 self.AI_villager[int(villa_pos[2])].set_target(
#                     (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#                 self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
#                 self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#                 self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#                 self.map.events.getting_resource()
#                 self.map.mining = True
#         if (resource == "Carrière de pierre"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
#                 if (dict_resource[i][1][i_th_time][0] < min_dictance):
#                     min_dictance = dict_resource[i][1][i_th_time][0]
#                     villa_pos = (dict_resource[i][1][i_th_time][1], dict_resource[i][1][i_th_time][2], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 return
#             else:

#                 self.AI_villager[int(villa_pos[2])].set_target(
#                     (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#                 self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
#                 self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#                 self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#                 self.map.events.getting_resource()
#                 self.map.mining = True
#         if (resource == "Or"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
#                 if (dict_resource[i][2][i_th_time][0] < min_dictance):
#                     min_dictance = dict_resource[i][2][i_th_time][0]
#                     villa_pos = (dict_resource[i][2][i_th_time][1], dict_resource[i][2][i_th_time][2], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 return
#             else:
#                 self.AI_villager[int(villa_pos[2])].set_target(
#                     (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#                 self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
#                 self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#                 self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#                 self.map.events.getting_resource()
#                 self.map.mining = True
#         if (resource == "Buisson"):
#             min_dictance = 100  # out_of_map
#             villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
#             for i in dict_resource.keys():
#                 if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
#                 if (dict_resource[i][3][i_th_time][0] < min_dictance):
#                     min_dictance = dict_resource[i][3][i_th_time][0]
#                     villa_pos = (dict_resource[i][3][i_th_time][1], dict_resource[i][3][i_th_time][2], i)
#             if (villa_pos == (-1, -1, -1)): return
#             if self.AI_villager[int(villa_pos[2])].map.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
#                 return
#             else:
#                 self.AI_villager[int(villa_pos[2])].set_target(
#                     (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
#                 self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
#                 self.map.list_mining.append(self.map.world[villa_pos[0]][villa_pos[1]])
#                 self.map.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
#                 self.map.events.getting_resource()
#                 self.map.mining = True

#     # ================================================================================================================================================================
#     # =============================================================         CREATE UNITS         =====================================================================
#     # ================================================================================================================================================================

#     def create_villager(self, pos):
#         if self.created_tc:
#             for i in range(-1, 3):
#                 for j in range(-1, 3):
#                     if not self.map.world[self.towncenter.pos[0] + i][self.towncenter.pos[1] + j]["collision"]:
#                         temp = Villager(self.map.world[self.towncenter.pos[0] + i][self.towncenter.pos[1] + j],
#                                         self.map, self.resource_man, "Red", False)
#                         self.AI_villager.append(temp)
#                         temp.set_target(pos)
#                         return
#                         # elif not self.map.world[self.towncenter.pos[0]][self.towncenter.pos[1] + 1]["collision"]:
#                 #     self.AI_villager.append(
#                 #         Villager(self.map.world[self.towncenter.pos[0]][self.towncenter.pos[1] + 1], self.map, self.resource_man, "Red", False))
#                 # elif not self.map.world[self.towncenter.pos[0] + 1][self.towncenter.pos[1]]["collision"]:
#                 #     self.AI_villager.append(
#                 #         Villager(self.map.world[self.towncenter.pos[0]][self.towncenter.pos[1]], self.map, self.resource_man, "Red", False))

#     # mining ressource x = villager x - 1
#     def check_villager(self):
#         for i in self.AI_villager:
#             if not self.map.world[i.pos[0] - 1][i.pos[1]]["collision"]:
#                 # print(i.in_work)
#                 i.in_work = False
#         self.get_resource("Arbre")
#         self.get_resource("Or")
#         self.get_resource("Carrière de pierre")
#         self.get_resource("Buisson")

#     # create an Archer for each Archery
#     def create_Archer(self, x, y):
#         for i in self.map.entities:
#             if i.name == "Archery" and i.team == "Red":
#                 a = Archer(self.map.world[i.pos[0]][i.pos[1] + 1], self.map, self.map.resource_man,
#                            "Red", False)
#                 self.map.list_troop.append(a)
#                 self.AI_unit.append(a)
#                 a.set_target((x, y))

#     # Create an Infrantryman for each Barracks
#     def create_Infantryman(self, x, y):
#         for i in self.map.entities:
#             if i.name == "Barracks" and i.team == "Red":
#                 a = Infantryman(self.map.world[i.pos[0]][i.pos[1] + 1], self.map, self.map.resource_man,
#                                 "Red", False)
#                 self.map.list_troop.append(a)
#                 self.AI_unit.append(a)
#                 a.set_target((x, y))




#     def create_Cavalier(self, x, y):
#         for i in self.map.entities:
#             if i.name == "Stable" and i.team == "Red":
#                 a = Cavalier(self.map.world[i.pos[0]][i.pos[1] + 1], self.map, self.map.resource_man,
#                                 "Red", False)
#                 self.map.list_troop.append(a)
#                 self.AI_unit.append(a)
#                 a.set_target((x, y))

#     # ================================================================================================================================================================
#     # =============================================================       ATTACK AND DEFENSE     =====================================================================
#     # ================================================================================================================================================================

#     def auto_attack(self):
#         for soldat in self.AI_unit:
#             atk_range = soldat.get_attack_range()
#             for targ in atk_range:
#                 targ_soldat = self.map.units[targ[0]][targ[1]]
#                 if ( targ_soldat is not None) and (targ_soldat.team == "Blue"):
#                     self.map.list_units_atk.append((soldat, targ_soldat))


#     def all_attack(self, x, y):
#         targ = None
#         li = self.find_target()
#         for it in li:
#             if x == 0 and y == 0 and it.name == "TownCenter":
#                 targ = it
#                 break
#             elif x == 0 and y == 1 and it.name == "Barracks":
#                 targ = it
#                 break
#             elif x == 0 and y == 2 and it.name == "Archery":
#                 targ = it
#                 break
#             elif x == 1 and y == 0 and it.name == "Stable":
#                 targ = it
#                 break
#         co = - 5
#         pos = targ.pos
#         for sol in self.AI_unit:
#             if sol.name == "Cavalier":
#                 sol.set_target((pos[0]+co,pos[1]))
#                 for x in range(sol.pos[0]-sol.range,sol.pos[0]+sol.range):
#                     for y in range(sol.pos[1]-sol.range,sol.pos[1]+sol.range):
#                         if self.map.units[x][y] is not None:
#                             self.map.list_units_atk.append((sol, self.map.units[x][y]))
#                             self.map.list_attacker_defender.append((sol, self.map.buildings[x][y]))
#                             co += 1
#             if sol.name == "Archer":
#                 sol.set_target((pos[0],pos[1]+co))
#                 for x in range(sol.pos[0]-sol.range,sol.pos[0]+sol.range):
#                     for y in range(sol.pos[1]-sol.range,sol.pos[1]+sol.range):
#                         if self.map.units[x][y] is not None:
#                             self.map.list_units_atk.append((sol, self.map.units[x][y]))
#                             co += 1



#     def auto_defense(self):
#         if self.all_in == True:
#             return
#         for soldat in self.AI_unit:
#             if soldat.health <= 20:
#                 if (soldat.pos[0] <= 3 and soldat.pos[1] <= 3):
#                     if not self.map.world[soldat.pos[0]+1][soldat.pos[1]+1]["collision"]:
#                         soldat.set_target((soldat.pos[0]+1,soldat.pos[1]+1))
#                         continue
#                     if self.map.world[soldat.pos[0]+1][soldat.pos[1]+1]["collision"]:
#                         soldat.set_target((soldat.pos[0]+2,soldat.pos[1]+2))
#                         continue
#                     if self.map.world[soldat.pos[0]+2][soldat.pos[1]+2]["collision"]:
#                         soldat.set_target((soldat.pos[0]+3,soldat.pos[1]+3))
#                         continue
#                 elif ( 3 < soldat.pos[0] <= 30 and soldat.pos[1] <= 3):
#                     if not self.map.world[soldat.pos[0]+1][soldat.pos[1]]["collision"]:
#                         soldat.set_target((soldat.pos[0]+1,soldat.pos[1]))
#                         continue
#                     if self.map.world[soldat.pos[0]+1][soldat.pos[1]]["collision"]:
#                         soldat.set_target((soldat.pos[0]+2,soldat.pos[1]))
#                         continue
#                     if self.map.world[soldat.pos[0]+2][soldat.pos[1]]["collision"]:
#                         soldat.set_target((soldat.pos[0]+3,soldat.pos[1]))
#                         continue
#                 elif ( 30 < soldat.pos[0] <= 46 and soldat.pos[1] <= 3):
#                     if not self.map.world[soldat.pos[0]-1][soldat.pos[1]]["collision"]:
#                         soldat.set_target((soldat.pos[0]-1,soldat.pos[1]))
#                         continue
#                     if self.map.world[soldat.pos[0]-1][soldat.pos[1]]["collision"]:
#                         soldat.set_target((soldat.pos[0]-2,soldat.pos[1]))
#                         continue
#                     if self.map.world[soldat.pos[0]-2][soldat.pos[1]]["collision"]:
#                         soldat.set_target((soldat.pos[0]-3,soldat.pos[1]))
#                         continue
#                 elif ( 30 < soldat.pos[0] <= 46 and 30 < soldat.pos[1] <= 46):
#                     if not self.map.world[soldat.pos[0]-1][soldat.pos[1]-1]["collision"]:
#                         soldat.set_target((soldat.pos[0]-1,soldat.pos[1]-1))
#                         continue
#                     if self.map.world[soldat.pos[0]-1][soldat.pos[1]-1]["collision"]:
#                         soldat.set_target((soldat.pos[0]-2,soldat.pos[1]-2))
#                         continue
#                     if self.map.world[soldat.pos[0]-2][soldat.pos[1]-2]["collision"]:
#                         soldat.set_target((soldat.pos[0]-3,soldat.pos[1]-3))
#                         continue

#                 else:
#                     if (not self.map.world[3][3]["collision"]) and (self.map.units[3][3] is not None):
#                         soldat.set_target((3,3))
#                         continue
#                     if (not self.map.world[4][4]["collision"]) and (self.map.units[4][4] is not None):
#                         soldat.set_target((4,4))
#                         continue
#                     if (not self.map.world[5][4]["collision"]) and (self.map.units[5][4] is not None):
#                         soldat.set_target((5,4))
#                         continue
#                     if (not self.map.world[4][5]["collision"]) and (self.map.units[4][5] is not None):
#                         soldat.set_target((4,5))
#                         continue
#                     if (not self.map.world[1][1]["collision"]) and (self.map.units[1][1] is not None):
#                         soldat.set_target((1,1))
#                         continue
#     # ================================================================================================================================================================
#     # =============================================================       TARGET RESEARCHING      ====================================================================
#     # ================================================================================================================================================================

#     def find_target(self):
#         list_target = []
#         for i in range(0,50):
#             for j in range(0,50):
#                 if self.map.buildings[i][j] is not None:
#                     if self.map.buildings[i][j].team == "Blue":
#                         list_target.append(self.map.buildings[i][j])

#         return list_target




#     # ================================================================================================================================================================
#     # =============================================================           NEXT AGE           =====================================================================
#     # ================================================================================================================================================================


#     def next_age(self):
#         self.age = 2
#         for budi in self.AI_batiment:
#             budi.passer_age()


#     # ================================================================================================================================================================
#     # =============================================================          ACTION OF AI        =====================================================================
#     # ================================================================================================================================================================
#     # action of AI
#     def action_json(self):
#         self.minute, self.second = self.game_time.get_time()
#         temps = ((self.minute) * 60 + self.second) - self.previous_time
#         self.time = "%02d:%02d" % (self.minute, self.second)
#         if temps >= 1:
#             self.previous_time = (self.minute) * 60 + self.second
#             if self.map.resource_man.starting_resources_AI["Wood"] < 50:
#                 self.get_resource("Arbre")
#             if self.map.resource_man.starting_resources_AI["Rock"] < 50:
#                 self.get_resource("Carrière de pierre")
#             if self.map.resource_man.starting_resources_AI["Gold"] < 50:
#                 self.get_resource("Or")
#             if self.map.resource_man.starting_resources_AI["Food"] < 50:
#                 self.get_resource("Buisson")
#             if self.time in self.data.keys():
#                 i = self.data[self.time]
#                 for j in i:
#                     action_l = list(j.keys())
#                     action = action_l[0]
#                     pos_l = list(j.values())
#                     pos = pos_l[0].split(",")
#                     pos[0], pos[1] = int(pos[0]), int(pos[1])

#                     if action_dict.get(action) < 5:  # construct
#                         act = self.function_list[action_dict.get(action)]
#                         act(pos[0], pos[1])
#                     elif action_dict.get(action) == 5:
#                         act = self.function_list[action_dict.get(action)]
#                         act(pos)
#                     elif action_dict.get(action) == 6:
#                         self.get_resource("Arbre")
#                         self.get_resource("Or")
#                         self.get_resource("Carrière de pierre")
#                         self.get_resource("Buisson")
#                     elif action_dict.get(action) == 7:
#                         self.next_age()
#                     elif action_dict.get(action) == 8:
#                         act = self.function_list[action_dict.get(action)]
#                         act(pos[0], pos[1])
#                     elif action_dict.get(action) == 9:
#                         act = self.function_list[action_dict.get(action)]
#                         act(pos[0],pos[1])
#                     elif action_dict.get(action) == 10:
#                         self.all_attack(pos[0], pos[1])
#                     else:
#                         print("U should update ur action")

#             self.check_villager()
#             self.auto_attack()
#             self.auto_defense()

# # _____________________________________________________________________________________________________________________________________________________________
