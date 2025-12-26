import math
import pygame
from game.Level_2.Herb_attack import HerbAttack
from game.Entities.NPCCarnivore import NPCCarnivore
from game.Entities.NPCHerbivore import NPCHerbivore
from game.Entities.Herbivore import Herbivore

def shoot_herbivore(game, max_dist=200, speed=600):
    if not getattr(game, "herb_attack_unlocked", False):
        return
    if not isinstance(game.player, Herbivore):
        return

    now = pygame.time.get_ticks()
    if now - game.herb_attack_last < game.herb_attack_cooldown:
        return

    px, py = game.player.rect.center
    target = None
    best_d2 = None

    for e in game.npc_group:
        if not isinstance(e, (NPCCarnivore, NPCHerbivore)):
            continue
        if getattr(e, "health", 1) <= 0:
            continue

        ex, ey = e.rect.center
        dx = ex - px
        dy = ey - py
        d2 = dx * dx + dy * dy
        if d2 > max_dist * max_dist:
            continue

        if best_d2 is None or d2 < best_d2:
            best_d2 = d2
            target = e

    if target is None:
        return

    tx, ty = target.rect.center
    dx = tx - px
    dy = ty - py
    length = math.hypot(dx, dy) or 1.0
    vx = dx / length * speed
    vy = dy / length * speed

    damage = getattr(game, "herb_attack_damage", 30)

    proj = HerbAttack(
        pos=(px, py),
        vel=(vx, vy),
        damage=damage,
        max_range=max_dist,
        groups=(game.projectiles,)
    )
    game.herb_attack_last = now