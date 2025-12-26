import random

from game.Entities.NPCHerbivore import NPCHerbivore
from game.GameLogic.NPC_spawner import spawn_npc_outside_view
from game.Level_2.Apply_level2_dmg_visuals import apply_level2_dmg_visuals
from game.Level_2.Apply_level2_hp_visuals import apply_level2_hp_visuals


def spawn_level2_herbivores(game, count):
    before = set(game.npc_group)

    for _ in range(count):
        spawn_npc_outside_view(game, NPCHerbivore)

    new_npcs = [
        npc for npc in game.npc_group
        if isinstance(npc, NPCHerbivore) and npc not in before
    ]

    for npc in new_npcs:
        if random.random() < 0.5:
            if hasattr(npc, "max_health"):
                npc.max_health += 150
                npc.health += 150
                npc.has_level2_upgrade = True
                apply_level2_hp_visuals(npc, hp_upgrade=True)
                apply_level2_dmg_visuals(npc, dmg_upgrade=False)

        else:
            if hasattr(npc, "attack_damage"):
                npc.attack_damage += 50
                npc.has_level2_upgrade = True
                apply_level2_dmg_visuals(npc, dmg_upgrade=True)
                apply_level2_hp_visuals(npc, hp_upgrade=False)