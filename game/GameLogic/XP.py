import pygame

from game.Level_2.Level_2_Spawner_Carn import spawn_level2_carnivores
from game.Level_2.Level_2_Spawner_Herb import spawn_level2_herbivores


def add_xp(game, amount):
    player = game.player
    old_level = player.get_level()
    player.xp += amount
    new_level = player.get_level()

    if new_level > old_level:
        game.current_level = new_level

        if new_level != 2:
            game.level_up_show = True
            game.level_up_start_time = pygame.time.get_ticks()

        player.max_health += 50
        player.health += 50

        for npc in game.npc_group:
            if hasattr(npc, "max_health") and hasattr(npc, "health"):
                npc.max_health += 50
                npc.health += 50

    if old_level < 2 <= new_level:
        game.next_state = "SECOND_LVL_UPGRADE"
        game.herb_attack_unlocked = True
        spawn_level2_carnivores(game, 10)
        spawn_level2_herbivores(game, 20)

    if new_level == 5:
        game.next_state = "END"