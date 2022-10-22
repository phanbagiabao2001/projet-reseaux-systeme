import pygame as pg
from settings import trajan


def draw_text(screen, text, size, colour, pos):
    font = pg.font.SysFont("serif", size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)
