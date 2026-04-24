import pygame
import sys
import random

pygame.init()

CELL_SIZE = 20
WIDTH = 600
HEIGHT = 400


CELL_W = WIDTH // CELL_SIZE
CELL_H = HEIGHT // CELL_SIZE


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 20)

# ----------- snake -----------
snake = [(5, 5), (4, 5), (3, 5)]  # segment coordinates
direction = (1, 0)  # right direction

# ----------- food -----------
def spawn_food():
    while True:
        pos = (random.randint(0, CELL_W - 1), random.randint(0, CELL_H - 1))
        if pos not in snake:
            return pos

food = spawn_food()

score = 0
level = 1
foods_eaten = 0
speed = 8

# ----------- main loop -----------
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # controls
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
    new_head = (head[0] + direction[0], head[1] + direction[1])

    # ----------- collide with walls -----------
    if (new_head[0] < 0 or new_head[0] >= CELL_W or
        new_head[1] < 0 or new_head[1] >= CELL_H):
        print("Game Over (wall)")
        pygame.quit()
        sys.exit()

    # ----------- collide with yourself -----------
    if new_head in snake:
        print("Game Over (self)")
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    # ----------- food eating-----------
    if new_head == food:
        score += 1
        foods_eaten += 1
        food = spawn_food()
    else:
        snake.pop()  
    # ----------- levels -----------
    
    if foods_eaten == 4:
        level += 1
        foods_eaten = 0
        speed += 2  

    # ----------- drawing -----------
    screen.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(screen, GREEN,
                         (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))


    pygame.draw.rect(screen, RED,
                     (food[0]*CELL_SIZE, food[1]*CELL_SIZE,
                      CELL_SIZE, CELL_SIZE))

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))

    pygame.display.flip()
    clock.tick(speed)