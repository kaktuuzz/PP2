import pygame
import sys
import random
import time

pygame.init()

# ----------- constants -----------
CELL_SIZE = 20
WIDTH = 600
HEIGHT = 400

CELL_W = WIDTH // CELL_SIZE
CELL_H = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Different food colors depending on weight
FOOD_TYPES = [
    {"color": (200, 0, 0), "value": 1, "lifetime": 8},   # normal food
    {"color": (255, 165, 0), "value": 2, "lifetime": 6}, # medium food
    {"color": (255, 255, 0), "value": 3, "lifetime": 4}, # rare food
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# ----------- snake -----------
snake = [(5, 5), (4, 5), (3, 5)]  # initial body
direction = (1, 0)  # moving right

# ----------- food system -----------

def spawn_food():
    
    #Spawn food with random position and random type (weight).
    #Returns a dictionary with position, value, color and spawn time.
    
    while True:
        pos = (random.randint(0, CELL_W - 1),
               random.randint(0, CELL_H - 1))
        if pos not in snake:
            food_type = random.choice(FOOD_TYPES)
            return {
                "pos": pos,
                "value": food_type["value"],
                "color": food_type["color"],
                "lifetime": food_type["lifetime"],
                "spawn_time": time.time()
            }

food = spawn_food()

# ----------- game stats -----------
score = 0
level = 1
foods_eaten = 0
speed = 8

# ----------- main loop -----------
while True:

    # ----------- events -----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # movement controls (prevent reverse direction)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # ----------- movement -----------
    head = snake[0]
    new_head = (head[0] + direction[0],
                head[1] + direction[1])

    # ----------- wall collision -----------
    if (new_head[0] < 0 or new_head[0] >= CELL_W or
        new_head[1] < 0 or new_head[1] >= CELL_H):
        print("Game Over (wall)")
        pygame.quit()
        sys.exit()

    # ----------- self collision -----------
    if new_head in snake:
        print("Game Over (self)")
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # ----------- food eating -----------
    if new_head == food["pos"]:
        # increase score depending on food weight
        score += food["value"]
        foods_eaten += 1
        food = spawn_food()
    else:
        snake.pop()

    # ----------- food timer (disappearing food) -----------
    current_time = time.time()
    if current_time - food["spawn_time"] > food["lifetime"]:
        # respawn food if time expired
        food = spawn_food()

    # ----------- level system -----------
    if foods_eaten == 4:
        level += 1
        foods_eaten = 0
        speed += 2  # increase snake speed

    # ----------- drawing -----------
    screen.fill(BLACK)

    # draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN,
            (segment[0] * CELL_SIZE,
             segment[1] * CELL_SIZE,
             CELL_SIZE, CELL_SIZE))

    # draw food (color depends on type)
    pygame.draw.rect(screen, food["color"],
        (food["pos"][0] * CELL_SIZE,
         food["pos"][1] * CELL_SIZE,
         CELL_SIZE, CELL_SIZE))

    # UI text
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))

    pygame.display.flip()
    clock.tick(speed)