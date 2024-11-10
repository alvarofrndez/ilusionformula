import pygame
import math
import random
from particles import ParticleSystem
import colors
import time

class Ball:
    def __init__(self, screen, circle):
        self.screen = screen
        self.circle = circle
        self.x, self.y = screen.width // 2, screen.height // 2
        self.radius = 10
        self.color = random.choice(colors.COLORS)
        self.speed_x = 10
        self.speed_y = 0
        self.gravity = 0.1
        self.number_of_collisions = 0
        self.total_collisions = 0
        self.last_bounce_time = time.time()
        self.particle_system = ParticleSystem(self.screen)

    def move(self):
        # Aplica la gravedad y mueve la bola
        self.speed_y += self.gravity + (self.radius / 1000)
        self.x += self.speed_x
        self.y += self.speed_y

        # Calcula la distancia al centro del círculo
        distance_to_center = math.sqrt((self.x - self.circle.center[0]) ** 2 + (self.y - self.circle.center[1]) ** 2)
        
        # Si la bola choca con el borde del círculo
        if distance_to_center + self.radius >= self.circle.radius:
            self.handleCollision(distance_to_center)

    def handleCollision(self, distance_to_center):
        # Incrementa el contador de colisiones y cambia el color
        self.number_of_collisions += 1
        self.color = random.choice(colors.COLORS)
        self.circle.color = self.color

        # Genera onda en el círculo
        self.circle.createWave()

        # Calcula el vector normal en el punto de colisión
        normal_x = (self.x - self.circle.center[0]) / distance_to_center
        normal_y = (self.y - self.circle.center[1]) / distance_to_center

        # Genera partículas en el punto de colisión
        self.particle_system.generateParticles(self.x, self.y)
        
        # Refleja la velocidad de la bola
        dot_product = self.speed_x * normal_x + self.speed_y * normal_y
        self.speed_x -= 2 * dot_product * normal_x
        self.speed_y -= 2 * dot_product * normal_y

        # Incrementa el radio de la bola y ajusta velocidad después de cierto número de colisiones
        if self.number_of_collisions >= 5:
            self.total_collisions += 0.5
            self.speed_x *= (1.25 * self.total_collisions - self.radius / 300)
            self.speed_y *= (1.25 * self.total_collisions - self.radius / 300)
            self.number_of_collisions = 0
        else:
            # Reduce la velocidad para simular pérdida de energía
            self.speed_x *= (0.99 - self.radius / 300)
            self.speed_y *= (0.99 - self.radius / 300)

        # Ajusta el radio de la bola
        if self.radius < self.circle.radius:
            self.radius += 2

        # Recoloca la bola para evitar que se quede pegada en el borde del círculo
        overlap = (distance_to_center + self.radius) - self.circle.radius
        self.x -= overlap * normal_x
        self.y -= overlap * normal_y

        # Actualiza el tiempo de la última colisión
        self.last_bounce_time = time.time()

    def draw(self):
        # Dibuja la bola en pantalla
        pygame.draw.circle(self.screen.window, self.color, (int(self.x), int(self.y)), self.radius)
        # Dibuja las partículas
        self.particle_system.draw(self.color)
