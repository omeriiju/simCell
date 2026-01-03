import math
import pygame
from game.Entities.NPCCarnivore import NPCCarnivore
from game.Entities.Herbivore import Herbivore
from game.Entities.Carnivore import Carnivore

from game.Level_2.Herb_attack import HerbAttack


def shoot_npc_herbivore(npc, game, max_dist=200, speed=600):
    px, py = npc.rect.center
    target = None
    best_d2 = None

    for e in game.npc_group:
        if not isinstance(e, NPCCarnivore):
            continue
        if e is npc:
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
        player = game.player
        if isinstance(player, (Carnivore, Herbivore)) and getattr(player, "health", 1) > 0:
            ex, ey = player.rect.center
            dx = ex - px
            dy = ey - py
            d2 = dx * dx + dy * dy
            if d2 <= max_dist * max_dist:
                target = player

    if target is None:
        return False

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
        groups=(game.projectiles,),
    )
    proj.owner = "npc"

    return True