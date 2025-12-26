import random
from game.Entities.NPCHerbivore import NPCHerbivore
from game.Camera import get_camera_rect
from game.Entities.NPCCarnivore import NPCCarnivore

def spawn_npc_outside_view(game, npc_type=None):
    camera_rect = get_camera_rect(game)

    while True:
        x = random.randint(0, game.map_width)
        y = random.randint(0, game.map_height)
        if not camera_rect.collidepoint(x, y):
            break

    if npc_type is None:
        npc_type = NPCHerbivore

    npc = npc_type(x,y)
    game.all_sprites.add(npc)
    game.npc_group.add(npc)