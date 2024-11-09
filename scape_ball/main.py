import pygame
from screen import Screen
from ball import Ball
from circle import Circle
import colors
import time
import random
import math
import songs

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(songs.SONG_PATH)
pygame.mixer.music.play(start=0)
pygame.mixer.music.pause()

# Configuración de pantalla y objetos
screen = Screen(900, 700)
circle_radius = 300
diss = .3
circles = [
    Circle(screen, circle_radius, random.choice(colors.COLORS), diss),
]
ball = Ball(screen, circles)

last_ring_spawn_time = time.time()
ring_spawn_interval = .5
interval = 0

running = True
game_over = False
clock = pygame.time.Clock()
FPS = 90

# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            pygame.mixer.music.pause()

    screen.clear()
    
    # Comprobar si se ha acabado el juego
    distance_to_center = math.sqrt((ball.x - ball.center[0]) ** 2 + (ball.y - ball.center[1]) ** 2)
    if len(circles) == 0 and distance_to_center + ball.radius >= circle_radius:
        running = False

    current_time = time.time()
    if current_time - last_ring_spawn_time >= ring_spawn_interval:
        color = random.choice(colors.COLORS)
        circles.append(Circle(screen, circle_radius, color, diss))
        last_ring_spawn_time = current_time
        diss += .01
        interval += 1
        if interval % 8 == 0:
            ring_spawn_interval -= .02

    # Comprobar si el juego termina
    # if ball.radius >= circle.radius:
    #     game_over = True

    # Movimiento de la bola y partículas
    ball.move()

    # Dibujar elementos
    ball.draw()

    for circle in circles:
        circle.draw()
    
    # Comprobaciones de música e imágenes
    # sound_manager.update(ball.last_bounce_time, screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
