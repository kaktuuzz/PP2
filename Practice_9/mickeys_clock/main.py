import pygame
import sys
from clock import clock

def main():
    pygame.init()
    
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Mouse Clock")
    
    clock_app = clock(WIDTH, HEIGHT)
    timer = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        clock_app.draw(screen)
        pygame.display.flip()
        timer.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()