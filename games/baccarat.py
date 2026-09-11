"""Neon Baccarat — player vs banker, colourful casino table."""
import random
import sys
import pygame

W, H = 900, 560
FELT = (8, 92, 58)
GOLD = (240, 200, 70)
WHITE = (245, 245, 250)
SUITS = {"S": "\u2660", "H": "\u2665", "D": "\u2666", "C": "\u2663"}
SCOL = {"S": (20, 20, 30), "C": (20, 80, 40), "H": (200, 30, 50), "D": (220, 80, 30)}


def deck():
    d = [(r, s) for s in "SHDC" for r in range(1, 14)]
    random.shuffle(d)
    return d


def value(card):
    r = card[0]
    if r >= 10:
        return 0
    return r


def hand_total(cards):
    return sum(value(c) for c in cards) % 10


def label(card):
    faces = {1: "A", 11: "J", 12: "Q", 13: "K"}
    return f"{faces.get(card[0], str(card[0]))}{SUITS[card[1]]}"


def draw_card(surf, font, card, x, y, face=True):
    rect = pygame.Rect(x, y, 78, 110)
    pygame.draw.rect(surf, WHITE if face else (40, 50, 140), rect, border_radius=8)
    pygame.draw.rect(surf, GOLD, rect, 2, border_radius=8)
    if face:
        col = SCOL[card[1]]
        t = font.render(label(card), True, col)
        surf.blit(t, (x + 8, y + 10))
        big = pygame.font.SysFont("segoe ui symbol", 36)
        s = big.render(SUITS[card[1]], True, col)
        surf.blit(s, (x + 24, y + 48))


def third_player(pt, p0):
    return pt <= 5


def third_banker(bt, pt, p2):
    if p2 is None:
        return bt <= 5
    pv = value(p2)
    if bt <= 2:
        return True
    if bt == 3:
        return pv != 8
    if bt == 4:
        return pv in (2, 3, 4, 5, 6, 7)
    if bt == 5:
        return pv in (4, 5, 6, 7)
    if bt == 6:
        return pv in (6, 7)
    return False


def deal_round(d):
    p = [d.pop(), d.pop()]
    b = [d.pop(), d.pop()]
    pt, bt = hand_total(p), hand_total(b)
    p3 = None
    if pt >= 8 or bt >= 8:
        return p, b, pt, bt
    if third_player(pt, p[0]):
        p3 = d.pop()
        p.append(p3)
        pt = hand_total(p)
    if third_banker(bt, pt, p3):
        b.append(d.pop())
        bt = hand_total(b)
    return p, b, pt, bt


def run():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Baccarat — ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    title = pygame.font.SysFont("consolas", 36, bold=True)
    cardf = pygame.font.SysFont("consolas", 20, bold=True)

    chips = 500
    bet = 25
    side = "player"
    msg = "Click PLAYER, BANKER or TIE, then DEAL"
    last = None
    cards_p, cards_b = [], []

    buttons = {
        "player": pygame.Rect(80, 470, 140, 48),
        "banker": pygame.Rect(240, 470, 140, 48),
        "tie": pygame.Rect(400, 470, 140, 48),
        "deal": pygame.Rect(580, 470, 140, 48),
        "plus": pygame.Rect(780, 470, 48, 48),
        "minus": pygame.Rect(730, 470, 48, 48),
    }

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if buttons["player"].collidepoint(e.pos):
                    side = "player"
                    msg = "Betting PLAYER"
                elif buttons["banker"].collidepoint(e.pos):
                    side = "banker"
                    msg = "Betting BANKER"
                elif buttons["tie"].collidepoint(e.pos):
                    side = "tie"
                    msg = "Betting TIE (8:1)"
                elif buttons["plus"].collidepoint(e.pos):
                    bet = min(chips, bet + 25)
                elif buttons["minus"].collidepoint(e.pos):
                    bet = max(25, bet - 25)
                elif buttons["deal"].collidepoint(e.pos) and chips >= bet:
                    d = deck()
                    cards_p, cards_b, pt, bt = deal_round(d)
                    if pt > bt:
                        win = "player"
                    elif bt > pt:
                        win = "banker"
                    else:
                        win = "tie"
                    last = (pt, bt, win)
                    if side == win:
                        payout = bet * 8 if win == "tie" else bet
                        if win == "banker":
                            payout = int(bet * 0.95)
                        chips += payout
                        msg = f"{win.upper()} wins {pt}-{bt}. You won {payout}"
                    else:
                        chips -= bet
                        msg = f"{win.upper()} wins {pt}-{bt}. Lost {bet}"
                    if chips < 25:
                        msg += "  —  bankroll empty"

        screen.fill(FELT)
        pygame.draw.ellipse(screen, (6, 70, 44), (40, 40, W - 80, 360), 0)
        pygame.draw.ellipse(screen, GOLD, (40, 40, W - 80, 360), 3)
        screen.blit(title.render("BACCARAT", True, GOLD), (W // 2 - 90, 16))
        screen.blit(font.render("PLAYER", True, WHITE), (160, 90))
        screen.blit(font.render("BANKER", True, WHITE), (560, 90))
        for i, c in enumerate(cards_p):
            draw_card(screen, cardf, c, 120 + i * 90, 130)
        for i, c in enumerate(cards_b):
            draw_card(screen, cardf, c, 520 + i * 90, 130)
        if last:
            screen.blit(font.render(f"P {last[0]}   B {last[1]}", True, GOLD), (W // 2 - 70, 280))
        screen.blit(font.render(f"CHIPS {chips}   BET {bet}   SIDE {side.upper()}", True, GOLD), (40, 420))
        screen.blit(font.render(msg, True, WHITE), (40, 444))

        cols = {"player": (50, 140, 255), "banker": (220, 50, 70), "tie": (200, 160, 40), "deal": (40, 180, 90)}
        for name, rect in buttons.items():
            col = cols.get(name, (80, 80, 90))
            if name == side:
                pygame.draw.rect(screen, (255, 255, 200), rect.inflate(6, 6), border_radius=8)
            pygame.draw.rect(screen, col, rect, border_radius=8)
            label_map = {"player": "PLAYER", "banker": "BANKER", "tie": "TIE", "deal": "DEAL", "plus": "+", "minus": "-"}
            t = font.render(label_map[name], True, WHITE)
            screen.blit(t, t.get_rect(center=rect.center))
        pygame.display.flip()


if __name__ == "__main__":
    run()
    sys.exit(0)
