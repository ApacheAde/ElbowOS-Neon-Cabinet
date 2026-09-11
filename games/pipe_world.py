"""Pipe World — original colourful platformer (not an emulator, not Mario)."""
import random
import sys
import pygame

W, H = 960, 540
GRAV = 0.55
JUMP = -11.5
SPEED = 4.4


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 36)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing = 1

    def update(self, tiles):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = SPEED
            self.facing = 1
        self.rect.x += int(self.vx)
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vx > 0:
                    self.rect.right = t.left
                elif self.vx < 0:
                    self.rect.left = t.right
        self.vy += GRAV
        self.rect.y += int(self.vy)
        self.on_ground = False
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vy > 0:
                    self.rect.bottom = t.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = t.bottom
                    self.vy = 0


def build_level():
    tiles = []
    coins = []
    foes = []
    flags = []
    ground_y = 460
    tiles.append(pygame.Rect(0, ground_y, 2400, 80))
    plats = [
        (220, 380, 140), (420, 320, 120), (620, 380, 100), (820, 300, 160),
        (1080, 360, 180), (1320, 280, 120), (1500, 360, 200), (1780, 300, 140), (2000, 380, 220),
    ]
    for x, y, w in plats:
        tiles.append(pygame.Rect(x, y, w, 22))
        coins.append(pygame.Rect(x + w // 2 - 8, y - 28, 16, 16))
    pipes = [(350, 400, 50, 60), (980, 400, 54, 60), (1680, 390, 50, 70)]
    for p in pipes:
        tiles.append(pygame.Rect(*p))
    for x in range(80, 2300, 180):
        coins.append(pygame.Rect(x, 420, 16, 16))
    for x in (500, 900, 1250, 1600, 1900):
        foes.append(pygame.Rect(x, ground_y - 28, 28, 28))
    flags.append(pygame.Rect(2280, 360, 18, 100))
    return tiles, coins, foes, flags


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pipe World — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    tiles, coins, foes, flags = build_level()
    foe_dir = [1] * len(foes)
    p = Player(40, 400)
    cam = 0
    score = 0
    lives = 3
    won = False
    sky_top, sky_bot = (70, 170, 255), (180, 230, 255)

    def reset_pos():
        p.rect.topleft = (40, 400)
        p.vx = p.vy = 0
        nonlocal cam
        cam = 0

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if p.on_ground and not won:
                    p.vy = JUMP
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                tiles, coins, foes, flags = build_level()
                foe_dir = [1] * len(foes)
                score, lives, won = 0, 3, False
                reset_pos()

        if lives > 0 and not won:
            p.update(tiles)
            cam = max(0, min(2400 - W, p.rect.centerx - W // 3))
            for c in coins[:]:
                if p.rect.colliderect(c):
                    coins.remove(c)
                    score += 10
            for i, f in enumerate(foes[:]):
                f.x += foe_dir[i] * 2
                if f.x < 200 or f.x > 2200:
                    foe_dir[i] *= -1
                if p.rect.colliderect(f):
                    if p.vy > 0 and p.rect.bottom - f.top < 18:
                        foes.remove(f)
                        foe_dir.pop(i)
                        p.vy = JUMP * 0.55
                        score += 50
                        break
                    else:
                        lives -= 1
                        reset_pos()
                        break
            for fl in flags:
                if p.rect.colliderect(fl):
                    won = True
            if p.rect.top > H + 40:
                lives -= 1
                reset_pos()

        screen.fill(sky_top)
        pygame.draw.rect(screen, sky_bot, (0, 220, W, H))
        for hx in range(-cam // 3, W, 180):
            pygame.draw.circle(screen, (50, 170, 80), (hx, 470), 90)
        for t in tiles:
            r = t.move(-cam, 0)
            if t.height > 50:
                pygame.draw.rect(screen, (40, 170, 70), r)
                pygame.draw.rect(screen, (30, 130, 50), (r.x - 6, r.y, r.w + 12, 16))
            elif t.height > 30:
                pygame.draw.rect(screen, (90, 200, 70), r)
            else:
                pygame.draw.rect(screen, (210, 90, 50), r, border_radius=3)
                pygame.draw.rect(screen, (160, 60, 30), r, 2, border_radius=3)
        for c in coins:
            pygame.draw.circle(screen, (255, 210, 40), (c.centerx - cam, c.centery), 9)
            pygame.draw.circle(screen, (255, 250, 180), (c.centerx - cam, c.centery), 4)
        for f in foes:
            pygame.draw.ellipse(screen, (160, 70, 40), f.move(-cam, 0))
            pygame.draw.circle(screen, (20, 10, 10), (f.centerx - cam - 6, f.y + 10), 3)
        for fl in flags:
            r = fl.move(-cam, 0)
            pygame.draw.rect(screen, (230, 230, 240), (r.x + 6, r.y, 6, r.h))
            pygame.draw.polygon(screen, (255, 60, 80), [(r.x + 12, r.y), (r.x + 48, r.y + 16), (r.x + 12, r.y + 32)])
        pr = p.rect.move(-cam, 0)
        pygame.draw.rect(screen, (255, 90, 70), pr, border_radius=6)
        pygame.draw.rect(screen, (40, 80, 200), (pr.x, pr.y + 20, pr.w, 16))
        eye_x = pr.centerx + (6 if p.facing > 0 else -6)
        pygame.draw.circle(screen, (255, 255, 255), (eye_x, pr.y + 12), 4)

        hud = f"SCORE {score}   LIVES {lives}   {'GOAL!' if won else ''}"
        screen.blit(font.render(hud, True, (20, 30, 40)), (18, 12))
        screen.blit(font.render("Arrows/WASD move  Space jump  R reset  Esc quit", True, (20, 30, 40)), (18, H - 28))
        if lives <= 0:
            t = font.render("DOWN AND OUT — R to retry", True, (180, 20, 40))
            screen.blit(t, (W // 2 - 160, 80))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
