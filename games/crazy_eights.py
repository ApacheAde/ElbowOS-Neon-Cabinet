"""Crazy Eights — colourful cards vs a simple CPU."""
import random
import sys
from collections import Counter
import pygame

W, H = 900, 600
BG = (16, 48, 36)
WHITE = (250, 250, 255)
GOLD = (240, 200, 70)
SUITS = ["\u2660", "\u2665", "\u2666", "\u2663"]
SCOL = {"\u2660": (25, 25, 35), "\u2663": (15, 90, 45), "\u2665": (200, 30, 50), "\u2666": (220, 80, 30)}
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def make_deck():
    d = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(d)
    return d


def playable(card, top, wild):
    r, s = card
    if r == "8":
        return True
    if r == top[0]:
        return True
    suit = wild if top[0] == "8" and wild else top[1]
    return s == suit


def cpu_choose(hand, top, wild):
    opts = [c for c in hand if playable(c, top, wild)]
    if not opts:
        return None
    eights = [c for c in opts if c[0] == "8"]
    normal = [c for c in opts if c[0] != "8"]
    return (normal or eights)[0]


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Crazy Eights — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    big = pygame.font.SysFont("consolas", 28, bold=True)
    cardf = pygame.font.SysFont("consolas", 18, bold=True)

    def reset():
        d = make_deck()
        you = [d.pop() for _ in range(7)]
        cpu = [d.pop() for _ in range(7)]
        pile = [d.pop()]
        while pile[-1][0] == "8":
            d.append(pile.pop())
            random.shuffle(d)
            pile.append(d.pop())
        return d, you, cpu, pile, None, "you", ""

    deck, you, cpu, pile, wild, turn, msg = reset()
    choosing_suit = False

    def card_rect(i, n, y):
        span = min(110, 700 // max(1, n))
        x = 60 + i * span
        return pygame.Rect(x, y, 86, 120)

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                deck, you, cpu, pile, wild, turn, msg = reset()
                choosing_suit = False
            if choosing_suit and e.type == pygame.KEYDOWN:
                mp = {pygame.K_1: "\u2660", pygame.K_2: "\u2665", pygame.K_3: "\u2666", pygame.K_4: "\u2663"}
                if e.key in mp:
                    wild = mp[e.key]
                    choosing_suit = False
                    turn = "cpu"
                    msg = f"Wild suit {wild}"
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and turn == "you" and not choosing_suit:
                if pygame.Rect(400, 220, 86, 120).collidepoint(e.pos):
                    if not deck:
                        deck = pile[:-1]
                        random.shuffle(deck)
                        pile = [pile[-1]]
                    if deck:
                        you.append(deck.pop())
                        msg = "Drew a card"
                        turn = "cpu"
                for i, c in enumerate(you):
                    if card_rect(i, len(you), 430).collidepoint(e.pos) and playable(c, pile[-1], wild):
                        you.remove(c)
                        pile.append(c)
                        if c[0] == "8":
                            choosing_suit = True
                            msg = "Choose suit: 1 spade 2 heart 3 diamond 4 club"
                        else:
                            wild = None
                            turn = "cpu"
                            msg = f"Played {c[0]}{c[1]}"
                        break

        if turn == "cpu" and not choosing_suit and you and cpu:
            pygame.time.delay(280)
            choice = cpu_choose(cpu, pile[-1], wild)
            if choice is None:
                if not deck:
                    deck = pile[:-1]
                    random.shuffle(deck)
                    pile = [pile[-1]]
                if deck:
                    cpu.append(deck.pop())
                    msg = "CPU draws"
            else:
                cpu.remove(choice)
                pile.append(choice)
                if choice[0] == "8":
                    suits = Counter(s for _, s in cpu) or Counter(SUITS)
                    wild = suits.most_common(1)[0][0]
                    msg = f"CPU eight -> {wild}"
                else:
                    wild = None
                    msg = f"CPU plays {choice[0]}{choice[1]}"
            turn = "you"

        if not you:
            msg = "YOU WIN — R to rematch"
            turn = "done"
        if not cpu:
            msg = "CPU WINS — R to rematch"
            turn = "done"

        screen.fill(BG)
        screen.blit(big.render("CRAZY EIGHTS", True, GOLD), (30, 16))
        screen.blit(font.render(f"CPU cards: {len(cpu)}    {msg}", True, WHITE), (30, 56))
        for i in range(len(cpu)):
            r = card_rect(i, max(len(cpu), 1), 90)
            pygame.draw.rect(screen, (40, 50, 140), r, border_radius=8)
            pygame.draw.rect(screen, GOLD, r, 2, border_radius=8)
        pygame.draw.rect(screen, (40, 50, 140), (400, 220, 86, 120), border_radius=8)
        screen.blit(font.render("DRAW", True, WHITE), (418, 268))
        top = pile[-1]
        pr = pygame.Rect(510, 220, 86, 120)
        pygame.draw.rect(screen, WHITE, pr, border_radius=8)
        pygame.draw.rect(screen, GOLD, pr, 2, border_radius=8)
        col = SCOL[top[1]]
        screen.blit(cardf.render(f"{top[0]}{top[1]}", True, col), (520, 250))
        suit_show = wild if top[0] == "8" and wild else top[1]
        screen.blit(font.render(f"Follow {suit_show} or rank or 8", True, GOLD), (400, 350))

        for i, c in enumerate(you):
            r = card_rect(i, len(you), 430)
            can = playable(c, pile[-1], wild) and turn == "you"
            pygame.draw.rect(screen, WHITE, r, border_radius=8)
            pygame.draw.rect(screen, (80, 220, 120) if can else (120, 120, 130), r, 3, border_radius=8)
            screen.blit(cardf.render(f"{c[0]}{c[1]}", True, SCOL[c[1]]), (r.x + 8, r.y + 12))
        screen.blit(font.render("Click a highlighted card or DRAW    R rematch    Esc quit", True, (200, 220, 200)), (30, H - 28))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
