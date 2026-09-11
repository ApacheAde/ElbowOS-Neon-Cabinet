# ElbowOS Neon Cabinet

Full-colour **Python 3** mini-games. Original titles only — this is **not** a Mario Bros / NES emulator and does not use Nintendo assets.

Featured: **[x.com/ElbowOS](https://x.com/ElbowOS)**

Repo: https://github.com/ApacheAde/ElbowOS-Neon-Cabinet

## Games

| Game | Kind | Run |
| --- | --- | --- |
| Pipe World | Original colourful platformer | `python games/pipe_world.py` |
| Neon Block Stack | Falling-block puzzle | `python games/block_stack.py` |
| Lily Dash | Frogger-style crossing | `python games/lily_dash.py` |
| Gem Crush | Match-3 | `python games/gem_crush.py` |
| Video Poker | Jacks or Better | `python games/video_poker.py` |
| Crazy Eights | Card game vs CPU | `python games/crazy_eights.py` |
| Baccarat | Casino table | `python games/baccarat.py` |
| Neon Keno | Lottery-style casino | `python games/keno.py` |

## Setup

```bash
python3 -m pip install -r requirements.txt
python3 launcher.py
```

Needs Python 3.10+ and [pygame](https://www.pygame.org/).

## Notes

- Casino games use play chips only. No real-money gambling.
- Platformer is an original plumber-in-pipes pastiche, not an emulator and not a Nintendo product.
- MIT licensed. Built for [ElbowOS](https://x.com/ElbowOS).
