import random
import pygame
import math
from .Entity import Entity
from game.GameLogic.Food import Meat

from game.Entities.NPCHerbivore import NPCHerbivore
from ..GameLogic.Food_spawner import spawn_food_outside_view

def random_direction():
    angle = random.uniform(0, 2 * math.pi)
    return math.cos(angle), math.sin(angle)

class NPCCarnivore(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "visuals/phase1/red_0.png")

        self.has_level2_upgrade = False

        scale = 0.2
        all_frames = []

        for i in range(2):
            img = pygame.image.load(f"visuals/phase1/red_{i}.png").convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
            all_frames.append(img)

        pattern = [0, 1]
        self.frames = [all_frames[i] for i in pattern]

        self.anim_index = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.25

        self.base_image = self.frames[0]
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 250
        self.seek_dist = 300

        self.wander_dx = 1.0
        self.wander_dy = 0.0
        self.wander_change_time = 0
        self.wander_interval = 3000

        self.max_health = 200
        self.health = self.max_health

        self.attack_cooldown = 600
        self.last_attack_time = 0
        self.attack_damage = 100

    def update(self, dt, food_group, world_rect, player, npc_group, game):
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer -= self.anim_speed
            self.anim_index = (self.anim_index + 1) % len(self.frames)
            self.base_image = self.frames[self.anim_index]

        now = pygame.time.get_ticks()

        target = None
        min_dist = float("inf")

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist < self.seek_dist:
            min_dist = dist
            target = player

        for npc in npc_group:
            if isinstance(npc, NPCHerbivore):
                dx = npc.rect.centerx - self.rect.centerx
                dy = npc.rect.centery - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist < self.seek_dist and dist < min_dist:
                    min_dist = dist
                    target = npc

        if target is None:
            for food in food_group:
                if isinstance(food, Meat):
                    dx = food.rect.centerx - self.rect.centerx
                    dy = food.rect.centery - self.rect.centery
                    dist = math.hypot(dx, dy)
                    if dist < self.seek_dist and dist < min_dist:
                        min_dist = dist
                        target = food

        if target is not None:
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > 0:
                dir_x = dx / dist
                dir_y = dy / dist

                angle = math.degrees(math.atan2(-dir_y, dir_x))
                current_frame = self.frames[self.anim_index]
                rotated = pygame.transform.rotate(current_frame, angle)
                old_center = self.rect.center
                self.image = rotated
                self.rect = self.image.get_rect(center=old_center)

                self.rect.x += dir_x * self.speed * dt * 0.8
                self.rect.y += dir_y * self.speed * dt * 0.8
        else:
            if now - self.wander_change_time > self.wander_interval:
                self.wander_change_time = now
                self.wander_dx, self.wander_dy = random_direction()

            dir_x = self.wander_dx
            dir_y = self.wander_dy

            angle = math.degrees(math.atan2(-dir_y, dir_x))
            current_frame = self.frames[self.anim_index]
            rotated = pygame.transform.rotate(current_frame, angle)
            old_center = self.rect.center
            self.image = rotated
            self.rect = self.image.get_rect(center=old_center)

            self.rect.x += dir_x * self.speed * dt * 0.8
            self.rect.y += dir_y * self.speed * dt * 0.8

        # zjadanie miesek
        for food in list(food_group):
            if isinstance(food, Meat) and self.rect.colliderect(food.rect):
                food_group.remove(food)
                spawn_food_outside_view(game, Meat)
                break

        self.rect.clamp_ip(world_rect)