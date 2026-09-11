"""Neon Block Stack — colourful falling-block puzzle (original, not Tetris)."""
import random
import sys
import pygame

W, H = 420, 640
COLS, ROWS = 10, 20
CELL = 28
OX, OY = 40, 40
BG = (12, 8, 28)
GRID = (36, 24, 62)

SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "L": [[1, 0], [1, 0], [1, 1]],
    "J": [[0, 1], [0, 1], [1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
}
COLORS = {
    "I": (80, 230, 255),
    "O": (255, 220, 70),
    "T": (210, 90, 255),
    "L": (255, 160, 50),
    "J": (80, 130, 255),
    "S": (80, 230, 120),
    "Z": (255, 80, 110),
}


def rotate(m):
    return [list(row) for row in zip(*m[::-1])]


class Piece:
    def __init__(self):
        self.kind = random.choice(list(SHAPES))
        self.grid = [row[:] for row in SHAPES[self.kind]]
        self.x = COLS // 2 - len(self.grid[0]) // 2
        self.y = 0
        self.color = COLORS[self.kind]


def collides(board, piece, dx=0, dy=0, grid=None):
    g = grid if grid is not None else piece.grid
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if not v:
                continue
            x, y = piece.x + c + dx, piece.y + r + dy
            if x < 0 or x >= COLS or y >= ROWS:
                return True
            if y >= 0 and board[y][x]:
                return True
    return False


def merge(board, piece):
    for r, row in enumerate(piece.grid):
        for c, v in enumerate(row):
            if v and piece.y + r >= 0:
                board[piece.y + r][piece.x + c] = piece.color


def clear_lines(board):
    kept = [row for row in board if any(cell is None for cell in row)]
    n = ROWS - len(kept)
    return [[None] * COLS for _ in range(n)] + kept, n


def draw_cell(surf, x, y, color, glow=True):
    rect = pygame.Rect(OX + x * CELL, OY + y * CELL, CELL - 2, CELL - 2)
    pygame.draw.rect(surf, color, rect, border_radius=4)
    if glow:
        hi = tuple(min(255, c + 50) for c in color)
        pygame.draw.rect(surf, hi, rect.inflate(-8, -8), border_radius=3)


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Block Stack — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 36, bold=True)

    board = [[None] * COLS for _ in range(ROWS)]
    piece = Piece()
    score = 0
    fall = 0
    speed = 480
    over = False

    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if over and e.key == pygame.K_r:
                    board = [[None] * COLS for _ in range(ROWS)]
                    piece = Piece()
                    score = 0
                    over = False
                    continue
                if over:
                    continue
                if e.key in (pygame.K_LEFT, pygame.K_a) and not collides(board, piece, -1, 0):
                    piece.x -= 1
                elif e.key in (pygame.K_RIGHT, pygame.K_d) and not collides(board, piece, 1, 0):
                    piece.x += 1
                elif e.key in (pygame.K_DOWN, pygame.K_s) and not collides(board, piece, 0, 1):
                    piece.y += 1
                    score += 1
                elif e.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                    rot = rotate(piece.grid)
                    if not collides(board, piece, 0, 0, rot):
                        piece.grid = rot

        if not over:
            fall += dt
            if fall >= speed:
                fall = 0
                if not collides(board, piece, 0, 1):
                    piece.y += 1
                else:
                    merge(board, piece)
                    board, n = clear_lines(board)
                    score += [0, 100, 300, 600, 1000][n]
                    speed = max(120, speed - n * 12)
                    piece = Piece()
                    if collides(board, piece):
                        over = True

        screen.fill(BG)
        pygame.draw.rect(screen, (20, 14, 42), (OX - 6, OY - 6, COLS * CELL + 10, ROWS * CELL + 10), border_radius=8)
        for r in range(ROWS):
            for c in range(COLS):
                pygame.draw.rect(screen, GRID, (OX + c * CELL, OY + r * CELL, CELL - 2, CELL - 2), 1, border_radius=3)
                if board[r][c]:
                    draw_cell(screen, c, r, board[r][c])
        if not over:
            for r, row in enumerate(piece.grid):
                for c, v in enumerate(row):
                    if v:
                        draw_cell(screen, piece.x + c, piece.y + r, piece.color)
        screen.blit(font.render(f"SCORE  {score}", True, (255, 230, 90)), (OX, 8))
        screen.blit(font.render("Arrows / WASD  R restart  Esc quit", True, (160, 150, 200)), (24, H - 28))
        if over:
            t = big.render("STACKED OUT — R", True, (255, 80, 140))
            screen.blit(t, t.get_rect(center=(W // 2, 24)))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
