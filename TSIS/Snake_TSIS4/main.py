import pygame
import sys
from config import *
from game import Game
from db import get_leaderboard, get_best_score

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

state = "username"
username = ""
game = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "username":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = Game(screen, username)
                    state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        elif state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction!=(0,1):
                    game.direction=(0,-1)
                elif event.key == pygame.K_DOWN and game.direction!=(0,-1):
                    game.direction=(0,1)
                elif event.key == pygame.K_LEFT and game.direction!=(1,0):
                    game.direction=(-1,0)
                elif event.key == pygame.K_RIGHT and game.direction!=(-1,0):
                    game.direction=(1,0)

    screen.fill(BLACK)

    if state == "username":
        screen.blit(font.render("Enter username:", True, WHITE),(200,150))
        screen.blit(font.render(username, True, WHITE),(200,180))

    elif state == "menu":
        screen.blit(font.render("1 - Play", True, WHITE),(250,150))
        screen.blit(font.render("2 - Leaderboard", True, WHITE),(250,180))
        screen.blit(font.render("ESC - Quit", True, WHITE),(250,210))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            game.reset()
            state = "game"
        if keys[pygame.K_2]:
            state = "leaderboard"
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    elif state == "game":
        alive = game.update()
        game.draw(font)

        if not alive:
            from db import save_score
            save_score(game.player_id, game.score, game.level)
            state = "game_over"

    elif state == "game_over":
        best = get_best_score(game.player_id)

        screen.blit(font.render(f"Game Over", True, WHITE),(250,140))
        screen.blit(font.render(f"Score: {game.score}", True, WHITE),(250,170))
        screen.blit(font.render(f"Best: {best}", True, WHITE),(250,200))
        screen.blit(font.render("R - Retry | M - Menu", True, WHITE),(200,230))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game.reset()
            state = "game"
        if keys[pygame.K_m]:
            state = "menu"

    elif state == "leaderboard":
        data = get_leaderboard()
        y = 100

        screen.blit(font.render("Leaderboard", True, WHITE),(230,50))

        for i, row in enumerate(data):
            txt = f"{i+1}. {row[0]} - {row[1]} (L{row[2]})"
            screen.blit(font.render(txt, True, WHITE),(150,y))
            y += 25

        screen.blit(font.render("ESC - Back", True, WHITE),(200,330))

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            state = "menu"

    pygame.display.flip()
    clock.tick(game.speed if game else 10)