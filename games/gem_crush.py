"""Gem Crush — colourful 8x8 match-3."""
import random
import sys
import pygame

N = 8
CELL = 64
PAD = 40
W = PAD * 2 + N * CELL
H = PAD * 2 + N * CELL + 50
COLORS = [
    (255, 70, 90),
    (80, 200, 255),
    (255, 210, 60),
    (120, 230, 90),
    (200, 90, 255),
    (255, 140, 50),
]
NAMES = ["RUBY", "AQUA", "GOLD", "LIME", "VIOLET", "AMBER"]


def new_board():
    b = [[random.randrange(len(COLORS)) for _ in range(N)] for _ in range(N)]
    for _ in range(20):
        m = find_matches(b)
        if not m:
            break
        for r, c in m:
            b[r][c] = random.randrange(len(COLORS))
    return b


def inb(r, c):
    return 0 <= r < N and 0 <= c < N


def find_matches(b):
    hits = set()
    for r in range(N):
        c = 0
        while c < N:
            k = 1
            while c + k < N and b[r][c + k] == b[r][c]:
                k += 1
            if k >= 3:
                for i in range(k):
                    hits.add((r, c + i))
            c += k
    for c in range(N):
        r = 0
        while r < N:
            k = 1
            while r + k < N and b[r + k][c] == b[r][c]:
                k += 1
            if k >= 3:
                for i in range(k):
                    hits.add((r + i, c))
            r += k
    return hits


def collapse(b):
    moved = False
    for c in range(N):
        stack = [b[r][c] for r in range(N) if b[r][c] is not None]
        pad = [None] * (N - len(stack))
        col = pad + stack
        for r in range(N):
            if b[r][c] != col[r]:
                moved = True
            b[r][c] = col[r]
        for r in range(N):
            if b[r][c] is None:
                b[r][c] = random.randrange(len(COLORS))
                moved = True
    return moved


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Gem Crush — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    board = new_board()
    selected = None
    score = 0
    moves = 25

    def cell_at(pos):
        x, y = pos
        c = (x - PAD) // CELL
        r = (y - PAD) // CELL
        if inb(r, c):
            return r, c
        return None

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and moves > 0:
                hit = cell_at(e.pos)
                if not hit:
                    continue
                if selected is None:
                    selected = hit
                elif selected == hit:
                    selected = None
                else:
                    r1, c1 = selected
                    r2, c2 = hit
                    if abs(r1 - r2) + abs(c1 - c2) == 1:
                        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                        matches = find_matches(board)
                        if matches:
                            moves -= 1
                            combo = 0
                            while True:
                                m = find_matches(board)
                                if not m:
                                    break
                                combo += len(m)
                                for r, c in m:
                                    board[r][c] = None
                                collapse(board)
                            score += combo * 10
                        else:
                            board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                    selected = None

        screen.fill((16, 10, 28))
        screen.blit(font.render(f"SCORE {score}    MOVES {moves}", True, (255, 220, 90)), (PAD, 10))
        for r in range(N):
            for c in range(N):
                x, y = PAD + c * CELL, PAD + r * CELL
                rect = pygame.Rect(x + 4, y + 4, CELL - 8, CELL - 8)
                pygame.draw.rect(screen, COLORS[board[r][c]], rect, border_radius=14)
                if selected == (r, c):
                    pygame.draw.rect(screen, (255, 255, 255), rect, 4, border_radius=14)
        if moves <= 0:
            t = font.render("OUT OF MOVES — Esc to quit", True, (255, 90, 140))
            screen.blit(t, (PAD, H - 36))
        else:
            screen.blit(font.render("Swap adjacent gems to match 3+", True, (180, 170, 210)), (PAD, H - 36))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
