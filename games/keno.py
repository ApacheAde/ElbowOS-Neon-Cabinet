"""Neon Keno — pick numbers, colourful draw."""
import random
import sys
import pygame

W, H = 820, 640
BG = (12, 20, 48)
GOLD = (255, 205, 70)
PAY = {0: 0, 1: 0, 2: 1, 3: 2, 4: 5, 5: 12, 6: 40, 7: 100, 8: 250, 9: 1000, 10: 2500}


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Keno — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    big = pygame.font.SysFont("consolas", 28, bold=True)

    cells = []
    for n in range(1, 81):
        r, c = divmod(n - 1, 10)
        cells.append((n, pygame.Rect(30 + c * 76, 80 + r * 50, 68, 42)))
    picked = set()
    drawn = set()
    hits = set()
    credits, bet = 200, 5
    msg = "Pick up to 10 numbers, then DRAW"

    draw_btn = pygame.Rect(30, 500, 160, 50)
    clear_btn = pygame.Rect(210, 500, 160, 50)

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if clear_btn.collidepoint(e.pos):
                    picked, drawn, hits = set(), set(), set()
                    msg = "Board cleared"
                elif draw_btn.collidepoint(e.pos) and picked and credits >= bet:
                    credits -= bet
                    drawn = set(random.sample(range(1, 81), 20))
                    hits = picked & drawn
                    pay = PAY.get(len(hits), 0) * bet
                    credits += pay
                    msg = f"{len(hits)} hits  •  paid {pay}"
                else:
                    for n, rect in cells:
                        if rect.collidepoint(e.pos):
                            if n in picked:
                                picked.remove(n)
                            elif len(picked) < 10:
                                picked.add(n)

        screen.fill(BG)
        screen.blit(big.render("NEON KENO", True, GOLD), (30, 20))
        screen.blit(font.render(f"CREDITS {credits}   BET {bet}   PICKED {len(picked)}/10", True, (230, 230, 255)), (260, 28))
        for n, rect in cells:
            if n in hits:
                col = (40, 200, 90)
            elif n in picked and n in drawn:
                col = (40, 200, 90)
            elif n in picked:
                col = (50, 110, 255)
            elif n in drawn:
                col = (200, 60, 80)
            else:
                col = (32, 42, 80)
            pygame.draw.rect(screen, col, rect, border_radius=8)
            pygame.draw.rect(screen, GOLD if n in picked else (70, 80, 120), rect, 2, border_radius=8)
            t = font.render(str(n), True, (250, 250, 255))
            screen.blit(t, t.get_rect(center=rect.center))
        pygame.draw.rect(screen, (40, 170, 90), draw_btn, border_radius=8)
        pygame.draw.rect(screen, (90, 90, 120), clear_btn, border_radius=8)
        screen.blit(font.render("DRAW 20", True, (255, 255, 255)), draw_btn.move(32, 14))
        screen.blit(font.render("CLEAR", True, (255, 255, 255)), clear_btn.move(48, 14))
        screen.blit(font.render(msg + "    Pays: 4=5x 5=12x 6=40x 7=100x 10=2500x", True, GOLD), (30, 570))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
