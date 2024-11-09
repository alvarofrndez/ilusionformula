import pygame
import random
import math
import colors

class ParticleSystem:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []

    def generateParticles(self, x, y):
        # Crear 30 partículas con posición inicial y velocidad aleatoria
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)  # Ángulo aleatorio
            speed = random.uniform(1, 2)  # Velocidad aleatoria
            vel_x = math.cos(angle) * speed  # Componente en X de la velocidad
            vel_y = math.sin(angle) * speed  # Componente en Y de la velocidad
            self.particles.append({
                "pos": [x, y],  # Posición inicial
                "vel": [vel_x, vel_y],  # Velocidad de la partícula
                "lifetime": random.randint(30, 50)  # Duración aleatoria de la partícula
            })

    def update(self):
        # Actualizar la posición de cada partícula y disminuir su vida
        for particle in self.particles[:]:
            # Actualizar la posición con la velocidad
            particle["pos"][0] += particle["vel"][0]
            particle["pos"][1] += particle["vel"][1]

            # Disminuir la vida de la partícula
            particle["lifetime"] -= 1

            # Eliminar la partícula si su vida ha llegado a cero
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)

    def draw(self, color):
        # Dibujar cada partícula en pantalla
        for particle in self.particles:
            pos = (int(particle["pos"][0]), int(particle["pos"][1]))
            pygame.draw.circle(self.screen.window, color, pos, 3)  # Dibujar cada partícula
