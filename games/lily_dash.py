"""Lily Dash — colourful frogger-style river crossing."""
import random
import sys
import pygame

W, H = 640, 720
BG = (8, 18, 36)
SAFE = (40, 90, 50)
WATER = (20, 70, 140)
ROAD = (40, 40, 48)
LILY = (50, 200, 90)
LOG = (150, 90, 40)
CAR_COLS = [(255, 70, 90), (255, 190, 50), (80, 200, 255), (220, 80, 255)]


class Actor:
    def __init__(self, x, y, w, h, vx, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.vx = vx
        self.color = color

    def update(self):
        self.rect.x += self.vx
        if self.vx > 0 and self.rect.left > W:
            self.rect.right = 0
        if self.vx < 0 and self.rect.right < 0:
            self.rect.left = W


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Lily Dash — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    lane_h = 48
    banks = [H - 72, H // 2 + 12, 48]
    frog = pygame.Rect(W // 2 - 16, banks[0] + 8, 32, 32)
    start = frog.copy()
    lives, score, goal = 3, 0, 0

    cars, logs = [], []
    for i, y in enumerate(range(banks[1] + lane_h, banks[0], lane_h)):
        vx = random.choice([-4, -3, 3, 4]) * (1 if i % 2 == 0 else -1)
        for k in range(3):
            cars.append(Actor(k * 240 + i * 40, y + 8, 70, 32, vx, random.choice(CAR_COLS)))
    for i, y in enumerate(range(banks[2] + lane_h, banks[1], lane_h)):
        vx = random.choice([-3, -2, 2, 3]) * (1 if i % 2 else -1)
        for k in range(3):
            w = random.choice([80, 100, 120])
            logs.append(Actor(k * 250 + i * 30, y + 10, w, 28, vx, LOG if i % 2 else LILY))

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and lives > 0:
                step = lane_h
                if e.key in (pygame.K_UP, pygame.K_w):
                    frog.y -= step
                    score += 2
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    frog.y = min(start.y, frog.y + step)
                elif e.key in (pygame.K_LEFT, pygame.K_a):
                    frog.x = max(8, frog.x - 40)
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    frog.x = min(W - 40, frog.x + 40)

        if lives > 0:
            for a in cars + logs:
                a.update()
            dead = False
            on_float = False
            if banks[2] < frog.centery < banks[1]:
                for lg in logs:
                    if frog.colliderect(lg.rect):
                        frog.x += lg.vx
                        on_float = True
                        break
                if not on_float:
                    dead = True
            for car in cars:
                if frog.colliderect(car.rect):
                    dead = True
            if frog.right < 0 or frog.left > W:
                dead = True
            if frog.top <= banks[2] + 8:
                goal += 1
                score += 100
                frog = start.copy()
            if dead:
                lives -= 1
                frog = start.copy()

        screen.fill(BG)
        pygame.draw.rect(screen, SAFE, (0, banks[0], W, H - banks[0]))
        pygame.draw.rect(screen, ROAD, (0, banks[1], W, banks[0] - banks[1]))
        pygame.draw.rect(screen, WATER, (0, banks[2], W, banks[1] - banks[2]))
        pygame.draw.rect(screen, SAFE, (0, 0, W, banks[2] + lane_h // 2))
        for lg in logs:
            pygame.draw.rect(screen, lg.color, lg.rect, border_radius=10)
        for car in cars:
            pygame.draw.rect(screen, car.color, car.rect, border_radius=6)
            pygame.draw.rect(screen, (240, 240, 255), (car.rect.x + 8, car.rect.y + 8, 12, 16))
        pygame.draw.ellipse(screen, (60, 230, 90), frog)
        pygame.draw.circle(screen, (20, 40, 20), (frog.x + 10, frog.y + 10), 4)
        pygame.draw.circle(screen, (20, 40, 20), (frog.x + 22, frog.y + 10), 4)
        hud = font.render(f"SCORE {score}   LIVES {lives}   GOALS {goal}", True, (255, 240, 120))
        screen.blit(hud, (16, 10))
        screen.blit(font.render("Arrows / WASD   Esc quit", True, (180, 200, 230)), (16, H - 28))
        if lives <= 0:
            t = font.render("SPLASHED — close window to exit", True, (255, 90, 130))
            screen.blit(t, (W // 2 - t.get_width() // 2, H // 2))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
