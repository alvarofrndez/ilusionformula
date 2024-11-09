import pygame
import colors

class Circle:
    def __init__(self, screen, radius, color, diss):
        self.screen = screen
        self.radius = radius
        self.color = color
        self.center = (screen.width // 2, screen.height // 2)
        self.diss = diss

    def draw(self):
        self.radius -= self.diss

        # Dibuja el círculo principal
        pygame.draw.circle(self.screen.window, self.color, self.center, self.radius, 3)
