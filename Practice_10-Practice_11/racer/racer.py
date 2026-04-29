import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
COIN_SCORE = 0  # total value from coins

# Speed increase condition
COINS_FOR_SPEED = 5  # increase speed every 5 coins

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Game")


# ---------- Enemy ----------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        #Respawn enemy at top with random X position
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        # If enemy leaves screen increase score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset_position()


# ---------- Player ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        #Handle player movement with keyboard
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


# ---------- Coin ----------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and scale coin image
        original_image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(original_image, (30, 30))
        self.rect = self.image.get_rect()

        # Random position
        self.reset_position()

        # -------- random weight/value --------
        self.value = random.choice([1, 2, 5])  # different coin weights

    def reset_position(self):
        #Respawn coin at top
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        #Move coin down the screen
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


# ---------- Objects ----------
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group(E1)

coins = pygame.sprite.Group()
for i in range(3):
    coins.add(Coin())

all_sprites = pygame.sprite.Group(P1, E1, *coins)


# ---------- Game Loop ----------
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))

    # Display score
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10,10))

    # Display collected coins count
    coin_text = font_small.render("Coins: " + str(COINS_COLLECTED), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 130, 10))

    # Display total coin value
    value_text = font_small.render("Value: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(value_text, (SCREEN_WIDTH - 130, 30))

    # Move and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # ---------- Coin Collection ----------
    collected = pygame.sprite.spritecollide(P1, coins, True)

    if collected:
        for coin in collected:
            COINS_COLLECTED += 1
            COIN_SCORE += coin.value  # add weighted value

        # Respawn new coins
        for i in range(len(collected)):
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        # -------- NEW: Increase speed based on coins --------
        if COINS_COLLECTED % COINS_FOR_SPEED == 0:
            SPEED += 1
            print("Speed increased! Current speed:", SPEED)

    # ---------- Collision with enemy ----------
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))

        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)