import pygame as pg
from settings import *
pg.init()
FONT = pg.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, resource_man, exit_box, text=''):

        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.resource_man = resource_man
        self.exit_box = exit_box
        self.total_text = ''
        self.bigdaddy = False
        self.fog = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:

                if event.key == pg.K_RETURN:
                    #Code for Resource
                    #coinage for gold
                    #pepperoni pizza for food
                    #quarry for rock
                    #woodstock for wood
                    #rock wood gold food plus facile à retenir

                    if self.text == 'ninjalui':
                        self.resource_man.starting_resources["Rock"] += 10000
                        self.resource_man.starting_resources["Wood"] += 10000
                        self.resource_man.starting_resources["Gold"] += 10000
                        self.resource_man.starting_resources["Food"] += 10000

                    if self.text == 'bigdaddy':
                        self.bigdaddy = True

                    if self.text == 'quarry':
                        self.resource_man.starting_resources["Rock"] += 100
                    if self.text == 'woodstock':
                        self.resource_man.starting_resources["Wood"] += 200
                    if self.text == 'coinage':
                        self.resource_man.starting_resources["Gold"] += 100
                    if self.text == 'pepperoni':
                        self.resource_man.starting_resources["Food"] += 100

                    #Code for No Fog
                    # if self.text == 'nofog':
                    #     if self.fog:
                    #         self.fog = False
                    #     else:
                    #         self.fog = True
                    self.text = ''
                    self.exit_box = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_ESCAPE:
                    self.exit_box = True

                else:
                    self.text += event.unicode
                # Re-render the text
                self.txt_surface = FONT.render(self.text, True, self.color)

            elif event.key == pg.K_ESCAPE:
                self.exit_box = True

    def update(self):
        # Resize the box if the text is too long.
        width = max(350, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

