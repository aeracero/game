import math
import random
import pygame
from starfall_pocket.animations import card_effect, motion, reveal
from starfall_pocket import render as R


@card_effect("bubbles")
def bubbles(ctx):
    rng = random.Random(str(ctx.card["id"]))
    for i in range(14):
        x = rng.uniform(0.1, 0.9) * ctx.w + math.sin(ctx.t * 2 + i) * 6 * ctx.k
        p = (ctx.t * rng.uniform(0.15, 0.3) + rng.random()) % 1
        y = ctx.h * (1.05 - p)
        pygame.draw.circle(ctx.layer, (255, 255, 255, int(160 * (1 - p))), (x, y), (4 + 6 * p) * ctx.k, max(1, int(2 * ctx.k)))


@motion("spin")
def spin(card, t):
    return 0, 0, 1.0, math.sin(t * 1.5) * 8


@reveal("confetti_rain")
def confetti_rain(ctx):
    if ctx.first:
        ctx.play("coin")
        ctx.flash(0.4)
    if random.random() < 0.8:
        ctx.burst(2, colors="rainbow", shape="confetti", speed=(10, 60), gravity=380,
                  x=random.uniform(0, ctx.screen.get_width()), y=-10)


@reveal("confetti_rain", front=True)
def confetti_rain_title(ctx):
    if ctx.elapsed < 1.5:
        R.outlined(ctx.screen, "WOW!", 60, (255, 230, 80), (60, 20, 0), center=(ctx.x, ctx.y - ctx.h / 2 - 34))
