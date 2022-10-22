import pygame as pg


class Camera:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.scroll = pg.Vector2(-4500, -1200)
        # self.scroll = pg.Vector2(-1500, -1400)
        self.dx = 0
        self.dy = 0
        self.speed = 20

    def update(self):

        mouse_pos = pg.mouse.get_pos()

        # x movement
        if mouse_pos[0] > self.width * 0.99:
            self.dx = - self.speed
        elif mouse_pos[0] < self.width * 0.01:
            self.dx = self.speed
        else:
            self.dx = 0

        # y movement
        if mouse_pos[1] > self.height * 0.99:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.01:
            self.dy = self.speed
        else:
            self.dy = 0

        # update camera scroll
        self.scroll.x += self.dx
        self.scroll.y += self.dy
