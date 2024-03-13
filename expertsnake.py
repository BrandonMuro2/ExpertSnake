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

# Colores y estado inicial
black, white, red, green = pygame.Color(0, 0, 0), pygame.Color(255, 255, 255), pygame.Color(255, 0, 0), pygame.Color(0, 255, 0)
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
direction = 'RIGHT'
score = 0
snake_speed = 15
move_counter = 0  # Contador de movimientos para generar obstáculos

# Obstáculos dinámicos
obstacles = []

# Direcciones
direction_deltas = {'UP': (0, -10), 'RIGHT': (10, 0), 'DOWN': (0, 10), 'LEFT': (-10, 0)}

def generate_obstacle():
    return {'pos': [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10], 'timer': 10}

# Frutas con efectos especiales
fruit_effects = {
    'normal': {'score': 10, 'effect': None},
    'speed_boost': {'score': 5, 'effect': 'increase_speed', 'duration': 100},
    'bonus_points': {'score': 20, 'effect': None}
}

def generate_fruit():
    fruit_type = random.choice(list(fruit_effects.keys()))
    pos = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
    return {'pos': pos, 'type': fruit_type, **fruit_effects[fruit_type]}

fruit_positions = [generate_fruit() for _ in range(5)]

def is_collision(point, exclude_head=True):
    if point[0] < 0 or point[0] >= window_x or point[1] < 0 or point[1] >= window_y:
        return True
    if point in (snake_body[1:] if exclude_head else snake_body):
        return True
    if point in [ob['pos'] for ob in obstacles]:
        return True
    return False

def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def choose_target_fruit():
    closest_fruit = min(fruit_positions, key=lambda x: distance(snake_position, x['pos']))
    return closest_fruit

def decide_direction(target_fruit):
    global direction
    best_direction = direction
    min_distance = float('inf')
    for dir, delta in direction_deltas.items():
        new_position = [snake_position[0] + delta[0], snake_position[1] + delta[1]]
        if not is_collision(new_position, exclude_head=False) and distance(new_position, target_fruit['pos']) < min_distance:
            best_direction = dir
            min_distance = distance(new_position, target_fruit['pos'])
    return best_direction

def apply_fruit_effect(fruit):
    global snake_speed
    effect = fruit['effect']
    if effect == 'increase_speed':
        snake_speed += 5  # Ejemplo: Aumenta la velocidad temporalmente
    # Implementa otros efectos según sea necesario

def update_snake(dir):
    global score, fruit_positions, snake_position, snake_body, running, move_counter
    delta = direction_deltas[dir]
    new_position = [snake_position[0] + delta[0], snake_position[1] + delta[1]]

    if is_collision(new_position, False):
        print("Collision detected. Game over.")
        running = False
        return

    snake_position = new_position
    snake_body.insert(0, list(snake_position))
    fruit_eaten = False

    for fruit in fruit_positions[:]:
        if snake_position == fruit['pos']:
            score += fruit['score']
            apply_fruit_effect(fruit)
            fruit_positions.remove(fruit)
            fruit_positions.append(generate_fruit())
            fruit_eaten = True
            break

    if not fruit_eaten:
        snake_body.pop()

    move_counter += 1
    if move_counter >= 100:
        obstacles.append(generate_obstacle())
        move_counter = 0

def draw_obstacles():
    for ob in obstacles[:]:
        pygame.draw.rect(game_window, white, pygame.Rect(ob['pos'][0], ob['pos'][1], 10, 10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    target_fruit = choose_target_fruit()
    direction = decide_direction(target_fruit)
    update_snake(direction)
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    for fruit in fruit_positions:
        pygame.draw.rect(game_window, red, pygame.Rect(fruit['pos'][0], fruit['pos'][1], 10, 10))
    draw_obstacles()
    
    score_surface = pygame.font.SysFont('times new roman', 20).render(f'Score : {score}', True, white)
    game_window.blit(score_surface, (0, 0))

    pygame.display.update()
    fps.tick(snake_speed)

pygame.quit()
