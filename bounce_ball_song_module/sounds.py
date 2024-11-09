import pygame
import time

class SoundManager:
    def __init__(self, song_path):
        pygame.mixer.init()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(start=0, loops=-1)

    def update(self, last_bounce_time, screen, bounce_threshold=0.3):

        if time.time() - last_bounce_time > bounce_threshold:
            pygame.mixer.music.play(start=0)
            # screen.window.blit(screen.main_image, (screen.width // 2 - 125, screen.height // 2 - 125))

        else:
            screen.window.blit(screen.secondary_image, (screen.width // 2 - 125, screen.height // 2 - 125))
