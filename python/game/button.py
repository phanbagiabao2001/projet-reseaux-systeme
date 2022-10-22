import pygame as pg


class Button:
    def __init__(self, screen, position, text, size, colors) -> None:
        self.screen = screen
        self.position = position
        self.text = text
        self.size = size
        self.colors = colors

    def button(self, color=""):
        if color == "":
            color = self.colors
        fg, bg = color.split(" on ")
        font = pg.font.SysFont("Arial", self.size)
        text_render = font.render(self.text, 1, fg)
        x, y, w, h = text_render.get_rect()
        x, y = self.position
        pg.draw.line(self.screen, (150, 150, 150), (x, y), (x + w, y), 5)
        pg.draw.line(self.screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pg.draw.line(self.screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
        pg.draw.line(self.screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
        self.rect = pg.draw.rect(self.screen, bg, (x, y, w, h))
        # print(self.screen.blit(text_render, (x, y)))
        return self.screen.blit(text_render, (x, y))

    def rect(self):
        return self.rect
