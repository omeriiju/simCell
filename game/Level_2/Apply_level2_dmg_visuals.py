import pygame
from game.Entities.NPCHerbivore import NPCHerbivore

def apply_level2_dmg_visuals(npc, dmg_upgrade=False):
    new_frames = []

    if isinstance(npc, NPCHerbivore):
        base_path = "visuals/phase2/green_dmg_" if dmg_upgrade else "visuals/phase2/green_dmg_"
        scale = 0.1
    else:
        base_path = "visuals/phase2/red_dmg_" if dmg_upgrade else "visuals/phase2/red_dmg_"
        scale = 0.1

    for i in range(2):
        img = pygame.image.load(f"{base_path}{i}.png").convert_alpha()
        w, h = img.get_size()
        img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
        new_frames.append(img)

    npc.frames = new_frames
    npc.anim_index = 0
    npc.anim_timer = 0.0
    npc.anim_speed = 0.25
    npc.base_image = npc.frames[0]
    old_center = npc.rect.center
    npc.image = npc.base_image
    npc.rect = npc.image.get_rect(center=old_center)
