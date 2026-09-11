"""Jacks or Better video poker — colourful 5-card draw."""
import random
import sys
from collections import Counter
import pygame

W, H = 860, 540
BG = (18, 12, 48)
GOLD = (255, 210, 70)
WHITE = (250, 250, 255)
SUITS = ["\u2660", "\u2665", "\u2666", "\u2663"]
SCOL = {"\u2660": (30, 30, 40), "\u2663": (20, 90, 50), "\u2665": (200, 35, 55), "\u2666": (230, 90, 30)}
RANKS = "A23456789TJQK"


def new_deck():
    d = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(d)
    return d


def rank_val(r):
    return {"A": 14, "T": 10, "J": 11, "Q": 12, "K": 13}.get(r, int(r))


def evaluate(hand):
    ranks = [c[0] for c in hand]
    suits = [c[1] for c in hand]
    vals = sorted(rank_val(r) for r in ranks)
    counts = Counter(ranks)
    flush = len(set(suits)) == 1
    unique = sorted(set(vals))
    straight = len(unique) == 5 and unique[-1] - unique[0] == 4
    if vals == [2, 3, 4, 5, 14]:
        straight = True
    royal = flush and set(ranks) == set("TJQKA")
    if royal:
        return "ROYAL FLUSH", 250
    if straight and flush:
        return "STRAIGHT FLUSH", 50
    if 4 in counts.values():
        return "FOUR OF A KIND", 25
    if sorted(counts.values()) == [2, 3]:
        return "FULL HOUSE", 9
    if flush:
        return "FLUSH", 6
    if straight:
        return "STRAIGHT", 4
    if 3 in counts.values():
        return "THREE OF A KIND", 3
    pairs = [r for r, n in counts.items() if n == 2]
    if len(pairs) == 2:
        return "TWO PAIR", 2
    if len(pairs) == 1 and rank_val(pairs[0]) >= 11:
        return "JACKS OR BETTER", 1
    return "NOTHING", 0


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Video Poker — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big = pygame.font.SysFont("consolas", 28, bold=True)
    cardf = pygame.font.SysFont("consolas", 26, bold=True)

    credits, bet = 100, 5
    deck = new_deck()
    hand = []
    held = [False] * 5
    phase = "deal"
    result = "Jacks or Better  -  hold cards then DRAW"

    def deal():
        nonlocal deck, hand, held, phase, result, credits
        if credits < bet:
            result = "Need more credits"
            return
        credits -= bet
        deck = new_deck()
        hand = [deck.pop() for _ in range(5)]
        held = [False] * 5
        phase = "draw"
        result = "Click cards to HOLD, then DRAW"

    def draw():
        nonlocal hand, phase, result, credits
        for i in range(5):
            if not held[i]:
                hand[i] = deck.pop()
        name, mult = evaluate(hand)
        win = bet * mult
        credits += win
        phase = "deal"
        result = f"{name}  +{win}" if win else f"{name}"

    card_rects = [pygame.Rect(50 + i * 155, 180, 140, 190) for i in range(5)]
    deal_btn = pygame.Rect(330, 430, 200, 56)

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if deal_btn.collidepoint(e.pos):
                    if phase == "deal":
                        deal()
                    else:
                        draw()
                elif phase == "draw":
                    for i, r in enumerate(card_rects):
                        if r.collidepoint(e.pos):
                            held[i] = not held[i]
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if phase == "deal":
                    deal()
                else:
                    draw()

        screen.fill(BG)
        pygame.draw.rect(screen, (28, 18, 70), (20, 20, W - 40, H - 40), border_radius=16)
        screen.blit(big.render("JACKS OR BETTER", True, GOLD), (40, 36))
        screen.blit(font.render(f"CREDITS {credits}    BET {bet}", True, WHITE), (40, 80))
        screen.blit(font.render(result, True, (180, 255, 200)), (40, 112))
        pay = "Royal 250  SF 50  Quads 25  Boat 9  Flush 6  Straight 4  Trips 3  2P 2  JoB 1"
        screen.blit(font.render(pay, True, (160, 150, 210)), (40, 144))

        for i, rect in enumerate(card_rects):
            pygame.draw.rect(screen, WHITE, rect, border_radius=12)
            pygame.draw.rect(screen, GOLD if (i < len(hand) and held[i]) else (80, 70, 120), rect, 4, border_radius=12)
            if i < len(hand):
                r, s = hand[i]
                col = SCOL[s]
                t = cardf.render(f"{r}{s}", True, col)
                screen.blit(t, t.get_rect(center=rect.center))
                if held[i]:
                    h = font.render("HOLD", True, (20, 140, 70))
                    screen.blit(h, h.get_rect(midbottom=(rect.centerx, rect.bottom - 10)))
            else:
                pygame.draw.rect(screen, (50, 40, 110), rect.inflate(-16, -16), border_radius=8)

        pygame.draw.rect(screen, (40, 170, 90) if phase == "deal" else (50, 110, 220), deal_btn, border_radius=10)
        label = "DEAL" if phase == "deal" else "DRAW"
        t = big.render(label, True, WHITE)
        screen.blit(t, t.get_rect(center=deal_btn.center))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
