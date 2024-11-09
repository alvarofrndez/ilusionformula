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
        self.main_image = pygame.image.load("assets/img1.png").convert_alpha()
        self.secondary_image = pygame.image.load("assets/img2.png").convert_alpha()
        self.main_image = pygame.transform.scale(self.main_image, (250, 250))
        self.secondary_image = pygame.transform.scale(self.secondary_image, (250, 250))

    def clear(self):
        self.window.fill(self.background_color)