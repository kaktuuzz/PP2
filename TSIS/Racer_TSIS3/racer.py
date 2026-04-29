import pygame, sys, random, json
from pygame.locals import *

pygame.init()

# ---------- SETTINGS ----------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

LANES = [80, 160, 240, 320]

base_speed = 5
SPEED = base_speed

MAX_ENEMIES = 4
MAX_OILS = 2
MAX_POWERUPS = 1

SCORE = 0
distance = 0

active_power = None
power_timer = 0

state = "name_input"
player_name = ""

# ---------- DISPLAY ----------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 40)
font_small = pygame.font.SysFont("Verdana", 20)

background = pygame.image.load("AnimatedStreet.png")

# ---------- PLAYER ----------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.centerx -= 5
        if keys[K_RIGHT]:
            self.rect.centerx += 5

        self.rect.clamp_ip(screen.get_rect())

# ---------- ENEMY ----------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.kill()

# ---------- OIL ----------
class Oil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("oil.png")
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# ---------- POWER UPS ----------
class Nitro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("boost.png")
        self.image = pygame.transform.scale(img, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("shield.png")
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# ---------- LEADERBOARD ----------
def save_score(name, score):
    try:
        with open("leaderboard.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({"name": name, "score": score})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open("leaderboard.json", "w") as f:
        json.dump(data, f)

def load_scores():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except:
        return []

# ---------- RESET ----------
def reset_game():
    global player, enemies, oils, nitros, shields, all_sprites
    global SCORE, SPEED, distance, active_power

    SCORE = 0
    SPEED = base_speed
    distance = 0
    active_power = None

    player = Player()

    enemies = pygame.sprite.Group()
    oils = pygame.sprite.Group()
    nitros = pygame.sprite.Group()
    shields = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group(player)

# ---------- MAIN LOOP ----------
reset_game()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if state == "name_input":
            if event.type == KEYDOWN:
                if event.key == K_RETURN and player_name != "":
                    state = "menu"
                elif event.key == K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        elif state == "menu":
            if event.type == KEYDOWN and event.key == K_RETURN:
                reset_game()
                state = "game"

        elif state == "game_over":
            if event.type == KEYDOWN and event.key == K_RETURN:
                state = "menu"

    screen.blit(background, (0, 0))

    # ---------- NAME INPUT ----------
    if state == "name_input":
        t1 = font.render("Enter Name:", True, (0,0,0))
        t2 = font.render(player_name, True, (0,0,255))
        screen.blit(t1, (80,200))
        screen.blit(t2, (80,260))

    # ---------- MENU ----------
    elif state == "menu":
        t = font.render("Press ENTER", True, (0,0,0))
        screen.blit(t, (80,250))

    # ---------- GAME ----------
    elif state == "game":

        # spawn enemies
        if len(enemies) < MAX_ENEMIES and random.randint(1,100) < 3:
            e = Enemy()
            enemies.add(e)
            all_sprites.add(e)

        # spawn oil
        if len(oils) < MAX_OILS and random.randint(1,100) < 2:
            o = Oil()
            oils.add(o)
            all_sprites.add(o)

        # spawn power-ups
        if len(nitros) + len(shields) < MAX_POWERUPS and random.randint(1,200) < 2:
            if random.choice([True, False]):
                n = Nitro()
                nitros.add(n)
                all_sprites.add(n)
            else:
                s = Shield()
                shields.add(s)
                all_sprites.add(s)

        # move + draw
        for e in all_sprites:
            screen.blit(e.image, e.rect)
            e.move()

        player.move()

        # collisions
        hit_enemy = pygame.sprite.spritecollideany(player, enemies)
        if hit_enemy:
            if active_power == "shield":
                hit_enemy.kill()
                active_power = None
            else:
                save_score(player_name, SCORE)
                state = "game_over"

        if pygame.sprite.spritecollideany(player, oils):
            player.rect.move_ip(random.choice([-40,40]), 0)

        if pygame.sprite.spritecollide(player, nitros, True):
            active_power = "nitro"
            power_timer = pygame.time.get_ticks()

        if pygame.sprite.spritecollide(player, shields, True):
            active_power = "shield"

        # power logic
        if active_power == "nitro":
            SPEED = base_speed + 3
            if pygame.time.get_ticks() - power_timer > 4000:
                SPEED = base_speed
                active_power = None

        # score
        distance += SPEED * 0.1

        screen.blit(font_small.render(f"Score: {SCORE}", True, (0,0,0)), (10,10))
        screen.blit(font_small.render(f"Dist: {int(distance)}", True, (0,0,0)), (10,30))
        screen.blit(font_small.render(f"Power: {active_power}", True, (0,0,0)), (10,50))

    # ---------- GAME OVER ----------
    elif state == "game_over":
        t = font.render("Game Over", True, (255,0,0))
        screen.blit(t, (80,200))

        scores = load_scores()
        y = 280
        for s in scores:
            line = font_small.render(f"{s['name']} : {s['score']}", True, (0,0,0))
            screen.blit(line, (100,y))
            y += 25

        screen.blit(font_small.render("Press ENTER", True, (0,0,0)), (120,500))

    pygame.display.update()
    clock.tick(FPS)