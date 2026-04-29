import pygame
import random
import time
from config import *
from db import *

class Game:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.player_id = get_or_create_player(username)

        self.reset()

    def reset(self):
        self.snake = [(5,5),(4,5),(3,5)]
        self.direction = (1,0)

        self.score = 0
        self.level = 1
        self.speed = 8
        self.base_speed = 8
        self.foods_eaten = 0

        self.food = self.spawn_food()
        self.poison = self.spawn_poison()

        self.powerup = None
        self.power_spawn_time = 0
        self.effect_end = 0
        self.active_effect = None
        self.shield = False

        self.obstacles = []

    def random_pos(self):
        return (random.randint(0, CELL_W-1),
                random.randint(0, CELL_H-1))

    def spawn_food(self):
        while True:
            pos = self.random_pos()
            if pos not in self.snake:
                return {"pos": pos}

    def spawn_poison(self):
        while True:
            pos = self.random_pos()
            if pos not in self.snake:
                return pos

    def spawn_power(self):
        types = ["speed","slow","shield"]
        return {
            "pos": self.random_pos(),
            "type": random.choice(types),
            "spawn": pygame.time.get_ticks()
        }

    def generate_obstacles(self):
        obs = []
        for _ in range(10):
            pos = self.random_pos()
            if pos not in self.snake:
                obs.append(pos)
        return obs

    def update(self):
        head = self.snake[0]
        new = (head[0]+self.direction[0],
               head[1]+self.direction[1])

        # collision
        if (new[0] < 0 or new[0] >= CELL_W or
            new[1] < 0 or new[1] >= CELL_H or
            new in self.snake or
            new in self.obstacles):
            
            if self.shield:
                self.shield = False
            else:
                return False

        self.snake.insert(0, new)

        # food
        if new == self.food["pos"]:
            self.score += 1
            self.foods_eaten += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        # poison
        if new == self.poison:
            for _ in range(2):
                if len(self.snake) > 0:
                    self.snake.pop()
            if len(self.snake) <= 1:
                return False
            self.poison = self.spawn_poison()

        # power spawn
        if not self.powerup and random.random() < 0.01:
            self.powerup = self.spawn_power()

        # power pickup
        if self.powerup and new == self.powerup["pos"]:
            t = self.powerup["type"]

            if t == "speed":
                self.speed = 15
                self.effect_end = pygame.time.get_ticks() + 5000
                self.active_effect = "speed"

            elif t == "slow":
                self.speed = 4
                self.effect_end = pygame.time.get_ticks() + 5000
                self.active_effect = "slow"

            elif t == "shield":
                self.shield = True

            self.powerup = None

        # effect end
        if self.active_effect and pygame.time.get_ticks() > self.effect_end:
            self.speed = self.base_speed
            self.active_effect = None

        # level
        if self.foods_eaten == 4:
            self.level += 1
            self.foods_eaten = 0
            self.speed += 1

            if self.level >= 3:
                self.obstacles = self.generate_obstacles()

        return True

    def draw(self, font):
        self.screen.fill(BLACK)

        for s in self.snake:
            pygame.draw.rect(self.screen, (0,200,0),
                (s[0]*CELL_SIZE, s[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(self.screen, (255,0,0),
            (self.food["pos"][0]*CELL_SIZE,
             self.food["pos"][1]*CELL_SIZE,
             CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(self.screen, (139,0,0),
            (self.poison[0]*CELL_SIZE,
             self.poison[1]*CELL_SIZE,
             CELL_SIZE, CELL_SIZE))

        if self.powerup:
            color = (0,255,255) if self.powerup["type"]=="speed" else (0,0,255) if self.powerup["type"]=="slow" else (255,255,255)
            pygame.draw.rect(self.screen, color,
                (self.powerup["pos"][0]*CELL_SIZE,
                 self.powerup["pos"][1]*CELL_SIZE,
                 CELL_SIZE, CELL_SIZE))

        for o in self.obstacles:
            pygame.draw.rect(self.screen, (100,100,100),
                (o[0]*CELL_SIZE, o[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        self.screen.blit(font.render(f"Score: {self.score}", True, WHITE),(10,10))
        self.screen.blit(font.render(f"Level: {self.level}", True, WHITE),(10,30))