import pygame
import math
import random
import colors
import time

class Ball:
    def __init__(self, screen, circles):
        self.screen = screen
        self.circles = circles
        self.x, self.y = screen.width // 2, screen.height // 2
        self.radius = 10
        self.color = random.choice(colors.COLORS)
        self.speed_x = 3
        self.speed_y = 0
        self.gravity = 0.1
        self.last_bounce_time = time.time()
        self.center = (screen.width // 2, screen.height // 2)
        self.increse = True

    def move(self):
        # Aplica la gravedad y mueve la bola
        self.speed_y += self.gravity + (self.radius / 1000)
        self.x += self.speed_x
        self.y += self.speed_y

        # Calcula la distancia al centro del círculo
        distance_to_center = math.sqrt((self.x - self.center[0]) ** 2 + (self.y - self.center[1]) ** 2)
        
        # Si la bola choca con el borde del círculo
        if len(self.circles) > 0 and distance_to_center + self.radius >= self.circles[0].radius:
            self.handleCollision(distance_to_center)

    def handleCollision(self, distance_to_center):
        # Incrementa el contador de colisiones y cambia el color
        self.color = random.choice(colors.COLORS)

        # Continuar la cancion
        pygame.mixer.music.unpause()
        pygame.time.set_timer(pygame.USEREVENT, 325)

        # Calcula el vector normal en el punto de colisión
        normal_x = (self.x - self.center[0]) / distance_to_center
        normal_y = (self.y - self.center[1]) / distance_to_center
        
        # Refleja la velocidad de la bola
        dot_product = self.speed_x * normal_x + self.speed_y * normal_y
        self.speed_x -= 2 * dot_product * normal_x
        self.speed_y -= 2 * dot_product * normal_y

        if self.increse:
            self.speed_x *= 1.02
            self.speed_y *= 1.02

        # Recoloca la bola para evitar que se quede pegada en el borde del círculo
        overlap = (distance_to_center + self.radius) - self.circles[0].radius
        self.x -= overlap * normal_x
        self.y -= overlap * normal_y

        # Actualiza el tiempo de la última colisión
        self.last_bounce_time = time.time()

        self.circles.remove(self.circles[0])

        self.increse != self.increse

    def draw(self):
        # Dibuja la bola en pantalla
        pygame.draw.circle(self.screen.window, self.color, (int(self.x), int(self.y)), self.radius)
