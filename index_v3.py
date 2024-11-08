import pygame
import math
import random
import time

# Inicializamos pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bola rebotando en el círculo")

# Colores
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
colors = [
    (255, 0, 0),  # Rojo
    (0, 255, 0),  # Verde
    (0, 0, 255),  # Azul
    (255, 255, 0),  # Amarillo
    (255, 105, 180),  # Rosa (Hot Pink)
    (0, 255, 255),  # Cian
    (255, 165, 0),  # Naranja
    (138, 43, 226),  # Azul Violeta
    (255, 105, 180),  # Rosa claro
]
last_color = BLUE

# Fondo de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def generateStars(star_count=0):
    stars = []
    for _ in range(star_count):
        # Generamos estrellas con posición y tamaño aleatorio
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)  # Tamaño de las estrellas
        color = (255, 255, 255, 0.3)   # Color claro
        stars.append((x, y, size, color))
    return stars

starts = generateStars()

# Centro y radio del círculo
circle_center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 200
circle_color = BLUE
thickness = 3

# Propiedades de la bola
ball_radius = 10  # Radio inicial de la bola
ball_color = BLUE
ball_x, ball_y = circle_center  # La bola comienza en el centro
ball_speed_x = 10  # Velocidad horizontal inicial
ball_speed_y = 0  # Velocidad vertical inicial
gravity = 0.1  # Gravedad base
number_of_collisions = 0
total_of_colissions = 0

# Cargar el sonido del rebote
rebound_sound = pygame.mixer.Sound("sounds/2806__thecheeseman__hurt-pain-sounds/44429__thecheeseman__hurt2.wav")

# Canción
pygame.mixer.init()
pygame.mixer.music.load("Clean Bandit - Symphony.mp3")  # Reemplaza con la ruta de tu canción
pygame.mixer.music.play(start=0, loops=-1)  # Reproduce la canción en bucle desde el principio

last_bounce_time = time.time()  # Guardar el momento del último rebote
bounce_threshold = .3  # Tiempo en segundos después del cual se reiniciará la canción

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Fuente para el texto
font = pygame.font.Font(None, 74)

# Lista para las ondas expansivas
waves = []

# Función para mover la bola
def moveBall():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, ball_radius, gravity, number_of_collisions, total_of_colissions, game_over
    
    # Aplicamos la gravedad a la velocidad vertical
    ball_speed_y += gravity + (ball_radius / 1000)  # Más grande = más gravedad

    # Calculamos el nuevo desplazamiento
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Distancia al centro del círculo
    distance_to_center = math.sqrt((ball_x - circle_center[0]) ** 2 + (ball_y - circle_center[1]) ** 2)
    
    # Comprobar el tiempo de la canción
    current_time = time.time()

    if (current_time - last_bounce_time > bounce_threshold):
        # Detener la canción si ha pasado el tiempo límite sin rebote
        pygame.mixer.music.stop()

    # Si la bola toca o pasa el borde del círculo
    if distance_to_center + ball_radius >= circle_radius:
        # Incrementamos el contador de colisiones
        number_of_collisions += 1

        # Reproducimos el sonido de rebote
        # rebound_sound.play()  

        # Cambiamos los colores de la bola y el círculo
        chooseNewColor()

        # Creamos una onda expansiva
        createWave()

        # Actualizar la canción
        updateSong()

        # Calculamos el vector normal en el punto de colisión
        normal_x = (ball_x - circle_center[0]) / distance_to_center
        normal_y = (ball_y - circle_center[1]) / distance_to_center
        
        # Calculamos el producto punto entre la velocidad y el vector normal
        dot_product = ball_speed_x * normal_x + ball_speed_y * normal_y
        
        # Reflejamos la velocidad de la bola usando la normal
        ball_speed_x = ball_speed_x - 2 * dot_product * normal_x
        ball_speed_y = ball_speed_y - 2 * dot_product * normal_y
        
        if number_of_collisions == 5:
            total_of_colissions += .5

            ball_speed_x *= (1.25 * total_of_colissions - ball_radius / 300)  # Menos rebote con bola más grande
            ball_speed_y *= (1.25 * total_of_colissions - ball_radius / 300)
            number_of_collisions = 0

        else:
            # Reducimos la velocidad en ambos ejes para simular pérdida de energía
            ball_speed_x *= (0.99 - ball_radius / 300)  # Menos rebote con bola más grande
            ball_speed_y *= (0.99 - ball_radius / 300)
        
        if game_over == False:
            # Incrementamos el tamaño de la bola
            ball_radius += 2
        
        # Reubicamos la bola un poco hacia el interior para evitar quedarse pegada al borde
        overlap = (distance_to_center + ball_radius) - circle_radius
        ball_x -= overlap * normal_x
        ball_y -= overlap * normal_y

def drawSmoothCircle(screen, color, position, radius):
    # Crear una superficie temporal más grande para el círculo
    # Crear una superficie temporal más grande para el círculo
    scale_factor = 4  # Factor de escala para hacer el círculo más grande
    large_radius = radius * scale_factor
    large_thickness = thickness * scale_factor
    temp_surface = pygame.Surface((large_radius * 2, large_radius * 2), pygame.SRCALPHA)

    # Dibujar el círculo hueco en la superficie temporal
    pygame.draw.circle(temp_surface, color, (large_radius, large_radius), large_radius, large_thickness)

    # Escalar la superficie hacia abajo y blit (dibujar) en la pantalla
    smooth_circle = pygame.transform.smoothscale(temp_surface, (radius * 2, radius * 2))
    screen.blit(smooth_circle, (position[0] - radius, position[1] - radius))

def drawSpaceBackground(screen, stars):
    screen.fill(BLACK) 
    for star in stars:
        x, y, size, color = star
        pygame.draw.circle(screen, color, (x, y), size)

def chooseNewColor():
    global ball_color, circle_color, last_color

    new_color = random.choice(colors)

    while new_color == last_color:
        new_color = random.choice(colors)
    
    ball_color = new_color
    circle_color = new_color
    last_color = new_color

def createWave():
    wave = {
        "radius": circle_radius,       # Empieza en el tamaño del círculo
        "color": circle_color,         # Color actual del círculo
        "alpha": 255,                  # Comienza completamente opaca
        "growth_rate": 5               # Velocidad de crecimiento de la onda
    }
    waves.append(wave)

def updateWaves():
    for wave in waves[:]:  # Iterar sobre una copia para eliminar sin problemas
        wave["radius"] += wave["growth_rate"]  # Incrementar el radio
        wave["alpha"] -= 5  # Reducir la opacidad gradualmente

        # Si la onda es completamente transparente, se elimina
        if wave["alpha"] <= 0:
            waves.remove(wave)
        else:
            # Dibujar la onda con la opacidad actual
            surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            color_with_alpha = (*wave["color"], wave["alpha"])
            pygame.draw.circle(surface, color_with_alpha, circle_center, int(wave["radius"]), 2)
            window.blit(surface, (0, 0))


def updateSong():
    global last_bounce_time, resume_position

    current_time = time.time()

    time_since_last_bounce = current_time - last_bounce_time

    if time_since_last_bounce > bounce_threshold:
        # Reiniciar la canción desde el principio si pasó mucho tiempo sin rebotar
        pygame.mixer.music.play(start=0)

    # Actualizar el tiempo del último rebote
    last_bounce_time = current_time

# Bucle principal del juego
running = True
game_over = False
time_start_game_over = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if ball_radius >= circle_radius:
        game_over = True

    # if not game_over:
    moveBall()
    
    # Dibujar el fondo
    drawSpaceBackground(screen, starts)

    # Dibujar el círculo
    drawSmoothCircle(window, circle_color, circle_center, circle_radius)
    pygame.draw.circle(window, circle_color, circle_center, circle_radius, 2)

    # Actualizar ondas expansivas
    updateWaves()
    
    # Dibujar la bola
    pygame.draw.circle(window, WHITE, (int(ball_x), int(ball_y)), ball_radius + 1)
    pygame.draw.circle(window, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    if game_over:
        if time_start_game_over == 0:
            time_start_game_over = time.time()

        if time.time() - time_start_game_over > 2:
            running = False
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar la velocidad de actualización
    clock.tick(90)

# Salir de pygame
pygame.time.delay(2000)
pygame.quit()