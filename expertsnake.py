import pygame
import random
import numpy as np
from math import sqrt

# Inicialización de pygame y configuración de la ventana
pygame.init()
window_x, window_y = 720, 480
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Snake Expert System')
fps = pygame.time.Clock()

# Colores
black, white, red, green = pygame.Color(0, 0, 0), pygame.Color(255, 255, 255), pygame.Color(255, 0, 0), pygame.Color(0, 255, 0)

# Estado inicial de la serpiente
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
direction = 'RIGHT'

# Frutas
fruit_positions = [[random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10] for _ in range(5)]

# Puntuación
score = 0

def is_collision(point, exclude_head=True):
    if point[0] < 0 or point[0] >= window_x or point[1] < 0 or point[1] >= window_y:
        return True
    if point in (snake_body[1:] if exclude_head else snake_body):
        return True
    return False

def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def choose_target_fruit():
    closest_fruit = None
    min_distance = float('inf')
    for fruit in fruit_positions:
        dist = distance(snake_position, fruit)
        if dist < min_distance:
            min_distance = dist
            closest_fruit = fruit
    return closest_fruit

def decide_direction(target_fruit):
    directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    direction_deltas = {'UP': (0, -10), 'RIGHT': (10, 0), 'DOWN': (0, 10), 'LEFT': (-10, 0)}
    best_direction = None
    min_distance_to_fruit = float('inf')
    
    for dir in directions:
        new_pos = [snake_position[0] + direction_deltas[dir][0], snake_position[1] + direction_deltas[dir][1]]
        if not is_collision(new_pos, False) and distance(new_pos, target_fruit) < min_distance_to_fruit:
            best_direction = dir
            min_distance_to_fruit = distance(new_pos, target_fruit)
    
    return best_direction if best_direction else direction  # Mantén la dirección actual si no hay una mejor opción

def update_snake(direction):
    global score, fruit_positions, snake_position, snake_body
    deltas = {'UP': (0, -10), 'RIGHT': (10, 0), 'DOWN': (0, 10), 'LEFT': (-10, 0)}
    new_position = [snake_position[0] + deltas[direction][0], snake_position[1] + deltas[direction][1]]

    # Verificar si la nueva posición causaría una colisión
    if is_collision(new_position, False):
        print("Colisión detectada. Fin del juego.")
        running = False  # Esto detendrá el bucle principal del juego
        return  # Salir de la función para evitar más procesamiento

    snake_position[0] += deltas[direction][0]
    snake_position[1] += deltas[direction][1]
    snake_body.insert(0, list(snake_position))

    if snake_position in fruit_positions:
        score += 10
        fruit_positions.remove(snake_position)
        fruit_positions.append([random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10])
    else:
        snake_body.pop()

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    target_fruit = choose_target_fruit()  # Elige la fruta objetivo
    direction = decide_direction(target_fruit)  # Sistema experto decide la próxima dirección
    update_snake(direction)  # Actualizar posición de la serpiente basado en la dirección decidida

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    for fruit_pos in fruit_positions:
        pygame.draw.rect(game_window, red, pygame.Rect(fruit_pos[0], fruit_pos[1], 10, 10))

    # Mostrar puntuación
    score_font = pygame.font.SysFont('times new roman', 20)
    score_surface = score_font.render('Score : ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

    pygame.display.update()
    fps.tick(15)

pygame.quit()
