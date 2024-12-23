import pygame
import math
import random
import time
import songs
import colors

# Inicializamos pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bola rebotando en el círculo")

# FPS
FPS = 90

# Colores
last_color = colors.BLUE

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
circle_color = colors.BLUE
thickness = 3

# Propiedades de la bola
ball_radius = 10  # Radio inicial de la bola
ball_color = colors.BLUE
ball_x, ball_y = circle_center  # La bola comienza en el centro
ball_speed_x = 10  # Velocidad horizontal inicial
ball_speed_y = 0  # Velocidad vertical inicial
gravity = 0.1  # Gravedad base
number_of_collisions = 0
total_of_colissions = 0

# Canción
pygame.mixer.init()
pygame.mixer.music.load(songs.SONG_PATH)  # Reemplaza con la ruta de tu canción
pygame.mixer.music.play(start=0, loops=-1)  # Reproduce la canción en bucle desde el principio

last_bounce_time = time.time()  # Guardar el momento del último rebote
bounce_threshold = .3  # Tiempo en segundos después del cual se reiniciará la canción

# Imagenes
main_image = pygame.image.load("img1.png")
secondary_image = pygame.image.load("img2.png")

main_image = pygame.transform.scale(main_image, (250, 250))
secondary_image = pygame.transform.scale(secondary_image, (250, 250))

image_rect = main_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Fuente para el texto
font = pygame.font.Font(None, 74)

# Lista para las ondas expansivas
waves = []

# Configuración de partículas
particles = []

# Función para mover la bola
def moveBall(type):
    global ball_x, ball_y, ball_speed_x, ball_speed_y, ball_radius, gravity
    
    # Aplicamos la gravedad a la velocidad vertical
    ball_speed_y += gravity + (ball_radius / 1000)  # Más grande = más gravedad

    # Calculamos el nuevo desplazamiento
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Distancia al centro del círculo
    distance_to_center = math.sqrt((ball_x - circle_center[0]) ** 2 + (ball_y - circle_center[1]) ** 2)

    # Si la bola toca o pasa el borde del círculo
    if distance_to_center + ball_radius >= circle_radius:
        checkCollision(distance_to_center, type)   

def checkCollision(distance_to_center, type):
    global ball_x, ball_y, ball_speed_x, ball_speed_y, ball_radius, gravity, number_of_collisions, total_of_colissions, game_over, circle_radius
    
    # Incrementamos el contador de colisiones
    number_of_collisions += 1

    # Cambiamos los colores de la bola y el círculo
    chooseNewColor()

    # Creamos una onda expansiva
    createWave()

    # Actualizar la canción
    updateSong()

    # Generar partículas
    if not game_over and type == 1:
        generateParticles(ball_x, ball_y)  # Generar partículas en el borde izquierdo

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
        if type == 0:
            circle_radius -= 1
        else:    
            ball_radius += 2
    
    # Reubicamos la bola un poco hacia el interior para evitar quedarse pegada al borde
    overlap = (distance_to_center + ball_radius) - circle_radius
    ball_x -= overlap * normal_x
    ball_y -= overlap * normal_y

def drawSmoothCircle(screen, color, position, radius, type, filled=False):
    # Crear una superficie temporal más grande para el círculo
    scale_factor = 4  # Factor de escala para hacer el círculo más grande
    large_radius = radius * scale_factor
    large_thickness = thickness * scale_factor
    temp_surface = pygame.Surface((large_radius * 2, large_radius * 2), pygame.SRCALPHA)

    # Dibujar el círculo hueco en la superficie temporal
    if not filled:
        pygame.draw.circle(temp_surface, color, (large_radius, large_radius), large_radius, large_thickness)

    else:
        pygame.draw.circle(temp_surface, color, (large_radius, large_radius), large_radius)
        if type == 0:
            pygame.draw.circle(temp_surface, colors.WHITE, (large_radius, large_radius), large_radius, 4)


    # Escalar la superficie hacia abajo y blit (dibujar) en la pantalla
    smooth_circle = pygame.transform.smoothscale(temp_surface, (radius * 2, radius * 2))
    screen.blit(smooth_circle, (position[0] - radius, position[1] - radius))

def drawSpaceBackground():
    screen.fill(colors.BLACK) 
    # for star in stars:
    #     x, y, size, color = star
    #     pygame.draw.circle(screen, color, (x, y), size)

def chooseNewColor():
    global ball_color, circle_color, last_color

    new_color = random.choice(colors.COLORS)

    while new_color == last_color:
        new_color = random.choice(colors.COLORS)
    
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

def checkSongAndImage(type):
    # Comprobar el tiempo de la canción
    current_time = time.time()

    if (current_time - last_bounce_time > bounce_threshold):
        # Detener la canción si ha pasado el tiempo límite sin rebote
        pygame.mixer.music.stop()
        # screen.blit(main_image, image_rect)
    else:
        if type == 1:
            screen.blit(secondary_image, image_rect)

def generateParticles(x, y):
    num_particles = 30  # Número de partículas que se crean
    for _ in range(num_particles):
        # Crear cada partícula con posición y velocidad aleatoria
        angle = random.uniform(0, 2 * math.pi)  # Ángulo aleatorio
        speed = random.uniform(1, 2)  # Velocidad aleatoria
        particle_vel_x = math.cos(angle) * speed
        particle_vel_y = math.sin(angle) * speed
        particles.append({
            "pos": [x, y],
            "vel": [particle_vel_x, particle_vel_y],
            "lifetime": random.randint(30, 50)  # Tiempo de vida de la partícula
        })

# Bucle principal del juego
running = True
game_over = False
time_start_game_over = 0

def start(type):
    global running, game_over, time_start_game_over

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if ball_radius >= circle_radius:
            game_over = True

        moveBall(type)
        
        # Dibujar el fondo
        if type == 1:
            drawSpaceBackground()

        # Dibujar el círculo
        drawSmoothCircle(window, circle_color, circle_center, circle_radius, type)

        # Actualizar ondas expansivas
        updateWaves()

        if type == 1:
            for particle in particles[:]:
                particle["pos"][0] += particle["vel"][0]
                particle["pos"][1] += particle["vel"][1]
                particle["lifetime"] -= 1
                if particle["lifetime"] <= 0:
                    particles.remove(particle)

            for particle in particles:
                pos = (int(particle["pos"][0]), int(particle["pos"][1]))
                pygame.draw.circle(screen, ball_color, pos, 3)

        # Dibujar la bola
        # pygame.draw.circle(window, WHITE, (int(ball_x), int(ball_y)), ball_radius + 1)
        drawSmoothCircle(window, ball_color, (ball_x, ball_y), ball_radius, type, True)

        checkSongAndImage(type)

        if game_over:
            if time_start_game_over == 0:
                time_start_game_over = time.time()

            if time.time() - time_start_game_over > 4:
                running = False
        
        # Actualizar la pantalla
        pygame.display.flip()
        
        # Controlar la velocidad de actualización
        clock.tick(FPS)

def end():
    # Salir de pygame
    pygame.quit()