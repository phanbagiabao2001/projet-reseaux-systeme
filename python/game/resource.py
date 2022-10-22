from .gui import *
from settings import *


class Resource:
    def __init__(self):

        self.starting_resources = {
            "Wood": STARTING_RESOURCES[0],
            "Rock": STARTING_RESOURCES[1],
            "Gold": STARTING_RESOURCES[2],
            "Food": STARTING_RESOURCES[3]
        }
        self.starting_resources_AI = {
            "Wood": STARTING_RESOURCES_AI[0],
            "Rock": STARTING_RESOURCES_AI[1],
            "Gold": STARTING_RESOURCES_AI[2],
            "Food": STARTING_RESOURCES_AI[3]
        }
        self.costs = {
            "TownCenter": {"Wood": 450, "Rock": 0, "Gold": 0, "Food": 0},
            "Barracks": {"Wood": 125, "Rock": 0, "Gold": 0, "Food": 0},
            "LumberMill": {"Wood": 50, "Rock": 0, "Gold": 0, "Food": 0},
            "Archery": {"Wood": 125, "Rock": 0, "Gold": 0, "Food": 0},
            "Stable": {"Wood": 150, "Rock": 0, "Gold": 0, "Food": 0},
            "Archer": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 20},
            "Infantryman": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 30},
            "Villager": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 50},
            "Cavalier": {"Wood": 0, "Rock": 0, "Gold": 75, "Food": 60},
            "Bigdaddy": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 0},
            "Secondage": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 800}
        }

        self.icons = {
            1: wood_icon,
            2: rock_icon,
            3: gold_icon,
            4: food_icon
        }

    def is_affordable(self, ent):
        affordable = True
        for resource, cost in self.costs[ent].items():
            if cost > self.starting_resources[resource]:
                affordable = False
        return affordable

    def buy(self, ent):
        achat = ent.name
        if ent.team == "Blue":
            for resource, cost in self.costs[achat].items():
                if self.starting_resources[resource] >= cost:
                    self.starting_resources[resource] -= cost
                else:
                    return -1
        elif ent.team == "Red":
            for resource, cost in self.costs[achat].items():
                if self.starting_resources_AI[resource] >= cost:
                    self.starting_resources_AI[resource] -= cost
                else:
                    return -1

    def buy_age(self, ent):

        achat = ent.age

        if ent.team == "Blue":
            for resource, cost in self.costs[achat].items():
                if self.starting_resources[resource] >= cost:
                    self.starting_resources[resource] -= cost
                else:
                    return -1
        elif ent.team == "Red":
            for resource, cost in self.costs[achat].items():
                if self.starting_resources_AI[resource] >= cost:
                    self.starting_resources_AI[resource] -= cost
                else:
                    return -1
