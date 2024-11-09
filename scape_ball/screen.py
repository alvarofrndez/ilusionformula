import pygame
import random
import colors

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bola rebotando en el círculo")
        self.background_color = colors.BLACK

    def clear(self):
        self.window.fill(self.background_color)