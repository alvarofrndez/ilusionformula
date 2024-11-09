import pygame
from screen import Screen
from ball import Ball
from circle import Circle
from particles import ParticleSystem
from sounds import SoundManager
import songs

pygame.init()

# Configuración de pantalla y objetos
screen = Screen(800, 600)
circle = Circle(screen, 200)
ball = Ball(screen, circle)
particles = ParticleSystem(screen)
sound_manager = SoundManager(songs.SONG_PATH)

running = True
game_over = False
clock = pygame.time.Clock()
FPS = 90

# Bucle principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.clear()

    # Comprobar si el juego termina
    if ball.radius >= circle.radius:
        game_over = True

    # Movimiento de la bola y partículas
    ball.move()
    circle.updateWaves()
    ball.particle_system.update()

    # Dibujar elementos
    ball.draw()
    circle.draw()
    
    # Comprobaciones de música e imágenes
    sound_manager.update(ball.last_bounce_time, screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
