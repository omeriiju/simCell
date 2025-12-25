import pygame

def add_xp(game, amount):
    player = game.player
    old_level = player.get_level()
    player.xp += amount
    new_level = player.get_level()

    if new_level > old_level:
        game.current_level = new_level
        game.level_up_show = True
        game.level_up_start_time = pygame.time.get_ticks()

        player.max_health += 50
        player.health += 50

        for npc in game.npc_group:
            if hasattr(npc, "max_health") and hasattr(npc, "health"):
                npc.max_health += 50
                npc.health += 50

    if new_level == 5:
        game.next_state = "END"