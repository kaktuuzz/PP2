import pygame

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.step = 20

    def move(self, key, width, height):
        if key == pygame.K_UP:
            if self.y - self.step - self.radius >= 0:
                self.y -= self.step

        if key == pygame.K_DOWN:
            if self.y + self.step + self.radius <= height:
                self.y += self.step

        if key == pygame.K_LEFT:
            if self.x - self.step - self.radius >= 0:
                self.x -= self.step

        if key == pygame.K_RIGHT:
            if self.x + self.step + self.radius <= width:
                self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)