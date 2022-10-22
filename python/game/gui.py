from settings import *
import pygame as pg
from .utils import draw_text
from os import path
from .button import *
from game.units import Archer, Infantryman, Villager
from game.buildings import *
from .resource import *


class Gui:

    def __init__(self, resource_man, width, height, events):

        self.resource_man = resource_man
        self.width = width
        self.height = height
        self.events = events
        self.gui_colour = GUI_COLOUR
        self.minimap_gui = GUI_MINIMAP_COLOUR
        self.pause = False
        border_width = 4

        # resource gui
        self.resources_surface = pg.Surface((width, height * 0.035), pg.SRCALPHA)
        self.resources_rect = self.resources_surface.get_rect(topleft=(0, 0))
        self.resources_surface.fill(self.gui_colour)
        pg.draw.rect(self.resources_surface, GUI_BORDER_COLOR,
                     [0, self.resources_rect.bottom - 3.5, self.resources_rect.right, border_width])  # bottom line

        # building gui
        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))
        self.build_surface.fill(self.gui_colour)
        pg.draw.rect(self.build_surface, GUI_BORDER_COLOR,
                     [0, 0, self.build_rect.right * 0.15, border_width])  # top line
        pg.draw.rect(self.build_surface, GUI_BORDER_COLOR,
                     [0, self.build_rect.bottom * 0.25 - 1, self.build_rect.right * 0.15, border_width])  # bottom line
        pg.draw.rect(self.build_surface, GUI_BORDER_COLOR,
                     [0, 0, border_width, self.build_rect.bottom * 0.25])  # left line
        pg.draw.rect(self.build_surface, GUI_BORDER_COLOR, [self.build_rect.right * 0.15 - 1, 0, border_width,
                                                            self.build_rect.bottom * 0.25 + border_width])  # right line

        self.icon_ligne = 1
        self.icon_colonne = 1

        # select gui
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.gui_colour)
        pg.draw.rect(self.select_surface, GUI_BORDER_COLOR, [0, 0, self.select_rect.right, border_width])  # top line
        pg.draw.rect(self.select_surface, GUI_BORDER_COLOR,
                     [0, self.select_rect.bottom * 0.2 - 1, self.select_rect.right, border_width])  # bottom line
        pg.draw.rect(self.select_surface, GUI_BORDER_COLOR,
                     [0, 0, border_width, self.select_rect.bottom * 0.25])  # left line
        pg.draw.rect(self.select_surface, GUI_BORDER_COLOR, [self.select_rect.right * 0.459, 0, border_width,
                                                             self.select_rect.bottom * 0.2 + border_width])  # right line

        # minimap gui
        self.minimap_surface = pg.Surface((width * 0.215, height * 0.25), pg.SRCALPHA)
        self.minimap_rect = self.minimap_surface.get_rect(topleft=(self.width * 0.024, self.height * 0.74))
        self.minimap_surface.fill(self.minimap_gui)
        pg.draw.rect(self.minimap_surface, GUI_BORDER_COLOR, [0, 0, self.minimap_rect.right, border_width])  # top line
        pg.draw.rect(self.minimap_surface, GUI_BORDER_COLOR,
                     [0, self.minimap_rect.bottom * 0.25 - 1, self.minimap_rect.right, border_width])  # bottom line
        pg.draw.rect(self.minimap_surface, GUI_BORDER_COLOR,
                     [0, 0, border_width, self.minimap_rect.bottom * 0.25])  # left line
        pg.draw.rect(self.minimap_surface, GUI_BORDER_COLOR, [self.minimap_rect.right * 0.89 - 1, 0, border_width,
                                                              self.minimap_rect.bottom * 0.25 + border_width])  # right line
        draw_text(self.minimap_surface, "Minimap", FONT_SIZE, WHITE,
                  (width * 0.088, 10))

        self.images = self.load_images()
        self.icon_images = self.load_icon_images(1)

        # create a new gui
        self.tiles = self.create_build_gui()

        self.age_sup = False

        # choose tree, rock or gold
        self.choose = None
        self.selecting_building = None
        self.examined_tile = None
        self.mining_gui = False
        self.examined_unit = None

    # afficher les batiments pour choisir et construire
    def create_build_gui(self):
        self.icon_colonne = 1
        self.icon_ligne = 1
        # position in the inventory
        render_pos = [self.width * 0.84 + self.build_surface.get_width() * 0.04,
                      self.height * 0.74 + self.build_surface.get_width() * 0.03]  # 0.84 0.74
        object_width = self.build_surface.get_width() // 4

        tiles = []
        # print('create_build_gui')
        for image_name, image in self.icon_images.items():  # ajouter l'image dans la fonction load_image()

            seconde_ligne = self.icon_colonne > 3 and self.icon_ligne == 1
            troisieme_ligne = self.icon_colonne > 3 and self.icon_ligne == 2

            if seconde_ligne:
                self.icon_colonne = 1
                self.icon_ligne = 2
                render_pos[0] = self.width * 0.84 + self.build_surface.get_width() * 0.04
                render_pos[1] = self.height * 0.82

            elif troisieme_ligne:
                self.icon_colonne = 1
                self.icon_ligne = 3
                render_pos[0] = self.width * 0.84 + self.build_surface.get_width() * 0.04
                render_pos[1] = self.height * 0.9

            # print('in for create_build_gui')
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            # choose the rect around the entity
            rect = image_scale.get_rect(topleft=pos)  # center

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True,
                    "ligne": self.icon_ligne,
                    "colonne": self.icon_colonne
                    # on peut ajouter plusieurs attributs ici
                }
            )

            # position in inventory for each entity
            render_pos[0] += image_scale.get_width() + self.build_surface.get_width() * 0.085

            self.icon_colonne += 1

        return tiles

    def update(self):
        # work in inventory
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        # unselect entity
        if mouse_action[2]:
            self.selecting_building = None

        for tile in self.tiles:
            if self.resource_man.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                # tile["rect"] is defined in create_build_gui()
                if mouse_action[0]:
                    self.selecting_building = tile

    def draw(self, screen):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        # minimap
        screen.blit(self.minimap_surface, (self.width * 0.024, self.height * 0.74))
        # bouton pause
        button6 = Button(screen, (self.width * 0.01, self.height * 0.05), '| |', 45, 'white on black')
        button6.button()
        # resource
        screen.blit(self.resources_surface, (0, 0))
        # build gui
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))
        # select gui

        if mouse_action[0] and button6.rect.collidepoint(mouse_pos):
            self.pause = True
            print("pause")

        if self.examined_unit is not None and (
                self.examined_unit.game_name in ("Archer", "Villageois", "Barbare", "Cavalier", "Bigdaddy")):

            img = self.examined_unit.image
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79)) # dessine le rectangle
                                                                            # regroupant les informations
            img_scale = self.scale_image(img, h=h * 0.70)
            health = format(str(self.examined_unit.health))
            health_max = format(str(self.examined_unit.health_max))
            draw_text(screen, f"Vie: {health} / {health_max}", FONT_SIZE, WHITE, # donne l'information de la vie de l'unité
                      (self.width * 0.35 + self.width * 0.17, self.height * 0.79 + self.height * 0.05))
            screen.blit(img_scale, (self.width * 0.35 + self.width * 0.008, self.height * 0.79 + self.height * 0.01))
            draw_text(screen, str(self.examined_unit.game_name), FONT_SIZE, WHITE, # donne son nom
                      (self.width * 0.35 + self.width * 0.17, self.height * 0.79 + self.height * 0.02))
            draw_text(screen, "{} team".format(self.examined_unit.team), FONT_SIZE, pg.Color(self.examined_unit.team),
                      (self.width * 0.35 + self.width * 0.25, self.height * 0.79 + self.height * 0.006)) # puis son équipe

            if mouse_action[2]: # action de déplacement (clic droit)
                self.events.change_unit_pos()

        if self.choose is not None and (not self.mining_gui) and self.choose["tile"] in (
        "Arbre", "Carrière de pierre", "Or", "Buisson"):
            img = self.choose["class"].image
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            img_scale = self.scale_image(img, h=h * 0.9)
            rest = self.choose["class"].the_rest
            rest_max = self.choose["class"].the_rest_max
            draw_text(screen, f"Reste: {rest} / {rest_max}", FONT_SIZE, GREEN,
                      (self.width * 0.35 + self.width * 0.17, self.height * 0.79 + self.height * 0.05))
            screen.blit(img_scale, (self.width * 0.35 + self.width * 0.008, self.height * 0.79 + self.height * 0.01))
            draw_text(screen, self.choose["tile"], FONT_SIZE * 2, WHITE,
                      (self.width * 0.35 + self.width * 0.17, self.height * 0.79 + self.height * 0.01))

        if self.examined_tile is not None:

            img = self.examined_tile.image
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            img_scale = self.scale_image(img, h=h * 0.7)
            screen.blit(img_scale, (self.width * 0.35 + self.width * 0.008, self.height * 0.79 + self.height * 0.04))
            # text in information box
            health = format(str(self.examined_tile.health))
            health_max = format(str(self.examined_tile.health_max))
            draw_text(screen, self.examined_tile.game_name, FONT_SIZE * 2, WHITE,
                      (self.select_rect.topleft[0] + 45, self.select_rect.topleft[1] + 6))
            draw_text(screen, f"Vie: {health} / {health_max}", FONT_SIZE, WHITE, self.select_rect.center)
            draw_text(screen, "{} team".format(self.examined_tile.team), FONT_SIZE, pg.Color(self.examined_tile.team),
                      (self.width * 0.35 + self.width * 0.25, self.height * 0.79 + self.height * 0.006))

            if self.examined_tile.name == "TownCenter" and self.examined_tile.team == "Blue":
                button = Button(screen, (self.width * 0.59, self.height * 0.95), 'Détruire', 20, 'white on red')
                button.button()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire le forum

                button2 = Button(screen, (self.width * 0.6 - 150, self.height * 0.95), 'Villageois', 20,
                                 'white on black')
                button2.button()
                if mouse_action[0] and button2.rect.collidepoint(mouse_pos):
                    button2.button("black on green")
                    self.events.remise()
                    self.events.create_troop('villager')
                    self.events.get_troop()  # retourne villager
                    # Code pour le bouton permettant de créer un villageois

                button3 = Button(screen, (self.width * 0.6 - 300, self.height * 0.9 + 60), 'Âge II', 15,
                                 'white on black')
                button3.button()
                # mouse_pos = pg.mouse.get_pos()
                # mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button3.rect.collidepoint(mouse_pos):
                    self.examined_tile.age_2 = True
                    self.events.remise()
                    button3.button("black on green")
                    self.events.set_age_sup()
                    self.age_sup = self.events.get_age_sup()

            if self.examined_tile.name == "Barracks" and self.examined_tile.team == "Blue":
                button = Button(screen, (self.width * 0.59, self.height * 0.95), 'Détruire', 20, 'white on red')
                button.button()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire la caserne

                button2 = Button(screen, (self.width * 0.6 - 150, self.height * 0.95), 'Barbare', 20,
                                 'white on black')
                button2.button()
                if mouse_action[0] and button2.rect.collidepoint(mouse_pos):
                    button2.button("black on green")
                    self.events.remise()
                    # print('Infantryman created')
                    self.events.create_troop('infantryman')
                    self.events.get_troop()
                    # Code pour le bouton permettant de créer un barbare

            if self.examined_tile.name == "Archery" and self.examined_tile.team == "Blue":
                button = Button(screen, (self.width * 0.59, self.height * 0.95), 'Détruire', 20, 'white on red')
                button.button()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire l'archerie

                button2 = Button(screen, (self.width * 0.6 - 150, self.height * 0.95), 'Archer', 20,
                                 'white on black')
                button2.button()
                if mouse_action[0] and button2.rect.collidepoint(mouse_pos):
                    button2.button("black on green")
                    self.events.remise()
                    # print('Archer created')
                    self.events.create_troop('archer')
                    self.events.get_troop()
                    # Code pour le bouton permettant de créer un archer

            if self.examined_tile.name == "Stable" and self.examined_tile.team == "Blue":
                button = Button(screen, (self.width * 0.59, self.height * 0.95), 'Détruire', 20, 'white on red')
                button.button()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire la caserne

                button2 = Button(screen, (self.width * 0.6 - 150, self.height * 0.95), 'Cavalier', 20,
                                 'white on black')
                button2.button()
                if mouse_action[0] and button2.rect.collidepoint(mouse_pos):
                    button2.button("black on green")
                    self.events.remise()
                    # print('Infantryman created')
                    self.events.create_troop('cavalier')
                    self.events.get_troop()
                    # Code pour le bouton permettant de créer un barbare

        # icon for entity selecting
        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

        # resource
        pos = self.width - 440  # resource info position
        cpt_res_icon = 1

        for resource, resource_value in self.resource_man.starting_resources.items():
            icon = self.resource_man.icons[cpt_res_icon]
            screen.blit(icon.convert_alpha(), (pos, self.height * 0.005))
            txt = "       : " + str(resource_value)
            draw_text(screen, txt, FONT_SIZE, WHITE, (pos, self.height * 0.01))
            pos += 110
            cpt_res_icon += 1

    def load_icon_images(self, age):
        TownCenter = towncenter_icon
        Barracks = barracks_icon
        Archery = archery_icon
        Stable = stable_icon

        images = {
            "TownCenter": TownCenter,
            "Barracks": Barracks,
            "Archery": Archery,
        }
        if age > 1: images.update({"Stable": Stable})
        return images

    def load_images(self):
        # read images
        # all images are saved in folder assets/graphics
        # Rock_image = Rock_img
        # Tree_image = Tree_img
        TownCenter = firstage_towncenter
        Barracks = firstage_barracks
        Archery = firstage_archery
        Stable = stable
        Archer = archer
        Infantryman = infantryman
        Villager = villager
        # tree = pg.image.load(path.join(graphics_folder,"tree.png"))
        # rock = pg.image.load(path.join(graphics_folder,"rock.png"))

        # load des images  d'unites ici
        # troop = pg.image.load(path.join(graphics_folder,"cart_E.png"))
        # troop_scale = self.scale_image(troop,self.build_surface.get_width() // 8)

        # on peut l'appeller sous le nom "image_name" comme dans la ligne 63
        images = {
            "TownCenter": TownCenter,
            "Barracks": Barracks,
            "Archery": Archery,
            "Stable": Stable
            # "tree": Tree_img,
            # "rock": Rock_img
            # "Archer" : Archer
            # "troop": troop
            # ajouter les images d'unites ici
            # example "troop": troop;
        }
        return images

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image
