"""ElbowOS Neon Cabinet — colourful Python 3 mini-games launcher."""
import os
import subprocess
import sys

import pygame

ROOT = os.path.dirname(os.path.abspath(__file__))
GAMES = os.path.join(ROOT, "games")

ITEMS = [
    ("Pipe World", "Original side-scroller (platforms, pipes, flag)", "pipe_world.py", (255, 90, 70)),
    ("Neon Block Stack", "Falling-block puzzle", "block_stack.py", (80, 230, 255)),
    ("Lily Dash", "River-road crossing", "lily_dash.py", (80, 230, 120)),
    ("Gem Crush", "Match-3 gems", "gem_crush.py", (200, 90, 255)),
    ("Video Poker", "Jacks or Better 5-card draw", "video_poker.py", (255, 210, 70)),
    ("Crazy Eights", "Shed cards vs CPU", "crazy_eights.py", (255, 160, 50)),
    ("Baccarat", "Player / Banker / Tie table", "baccarat.py", (50, 180, 110)),
    ("Neon Keno", "Pick 10, draw 20", "keno.py", (80, 130, 255)),
]


def launch(script):
    path = os.path.join(GAMES, script)
    pygame.quit()
    subprocess.call([sys.executable, path])
    pygame.init()
    pygame.display.set_caption("ElbowOS Neon Cabinet")


def run():
    pygame.init()
    screen = pygame.display.set_mode((720, 640))
    pygame.display.set_caption("ElbowOS Neon Cabinet")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("consolas", 34, bold=True)
    font = pygame.font.SysFont("consolas", 20)
    small = pygame.font.SysFont("consolas", 16)

    buttons = []
    for i, item in enumerate(ITEMS):
        buttons.append(pygame.Rect(60, 90 + i * 58, 600, 50))

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(e.pos):
                        launch(ITEMS[i][2])
                        screen = pygame.display.set_mode((720, 640))
            if e.type == pygame.KEYDOWN and e.key in range(pygame.K_1, pygame.K_9):
                idx = e.key - pygame.K_1
                if 0 <= idx < len(ITEMS):
                    launch(ITEMS[idx][2])
                    screen = pygame.display.set_mode((720, 640))

        screen.fill((10, 8, 24))
        pygame.draw.rect(screen, (28, 18, 60), (24, 16, 672, 608), border_radius=16)
        screen.blit(title.render("ELBOWOS NEON CABINET", True, (255, 220, 80)), (70, 28))
        screen.blit(small.render("https://x.com/ElbowOS    https://github.com/ApacheAde", True, (170, 160, 210)), (70, 64))
        mouse = pygame.mouse.get_pos()
        for i, rect in enumerate(buttons):
            name, blurb, _, col = ITEMS[i]
            bg = tuple(min(255, c + 30) for c in (30, 22, 55)) if rect.collidepoint(mouse) else (30, 22, 55)
            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, col, (rect.x, rect.y, 10, rect.h), border_radius=4)
            screen.blit(font.render(f"{i+1}  {name}", True, col), (rect.x + 24, rect.y + 6))
            screen.blit(small.render(blurb, True, (200, 200, 220)), (rect.x + 24, rect.y + 28))
        screen.blit(small.render("Click a game or press 1-8    Esc quits", True, (160, 150, 200)), (70, 600))
        pygame.display.flip()


if __name__ == "__main__":
    run()
