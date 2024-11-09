import pygame
import colors

class Circle:
    def __init__(self, screen, radius):
        self.screen = screen
        self.radius = radius
        self.color = colors.BLUE
        self.center = (screen.width // 2, screen.height // 2)
        self.waves = []  # Lista de ondas expansivas

    def draw(self):
        # Dibuja el círculo principal
        pygame.draw.circle(self.screen.window, self.color, self.center, self.radius, 3)
        
    def createWave(self):
        # Crear una nueva onda expansiva en el borde del círculo
        wave = {
            "radius": self.radius,       # Comienza en el tamaño del círculo
            "color": self.color,         # Color actual del círculo
            "alpha": 255,                # Opacidad inicial
            "growth_rate": 5             # Velocidad de crecimiento de la onda
        }
        self.waves.append(wave)  # Añadir la onda a la lista de ondas expansivas

    def updateWaves(self):
        # Actualizar y dibujar cada onda expansiva
        for wave in self.waves[:]:  # Iterar sobre una copia de la lista para eliminar sin problemas
            wave["radius"] += wave["growth_rate"]  # Incrementar el radio de la onda
            wave["alpha"] -= 5  # Reducir la opacidad de la onda gradualmente

            # Si la onda es completamente transparente, se elimina
            if wave["alpha"] <= 0:
                self.waves.remove(wave)
            else:
                # Dibujar la onda con transparencia
                self.draw_wave(wave)

    def draw_wave(self, wave):
        # Crear una superficie temporal con transparencia
        surface = pygame.Surface((self.screen.width, self.screen.height), pygame.SRCALPHA)
        color_with_alpha = (*wave["color"], wave["alpha"])
        pygame.draw.circle(surface, color_with_alpha, self.center, int(wave["radius"]), 2)
        
        # Dibujar la superficie temporal en la pantalla principal
        self.screen.window.blit(surface, (0, 0))
