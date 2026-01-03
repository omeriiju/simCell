import random
import pygame
import math

from game.Entities.Entity import Entity
from game.GameLogic.Food import Plant
from game.Entities.Carnivore import Carnivore
from game.GameLogic.Food_spawner import spawn_food_outside_view

def random_direction():
    angle = random.uniform(0, 2 * math.pi)
    return math.cos(angle), math.sin(angle)

class NPCHerbivore(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "visuals/phase1/green_0.png")

        self.has_level2_upgrade = False
        self.herb_attack_cooldown = 2000
        self.last_herb_attack = 0

        scale = 0.2
        all_frames = []

        for i in range(2):
            img = pygame.image.load(f"visuals/phase1/green_{i}.png").convert_alpha()
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
        self.seek_dist = 400

        self.wander_dx = 1.0
        self.wander_dy = 0.0
        self.wander_change_time = 0
        self.wander_interval = 3000

        self.max_health = 200
        self.health = self.max_health

        self.fear_dist = 300

    def update(self, dt, food_group, world_rect, player, game):
        self.anim_timer += dt
        if self.anim_timer >= self.anim_speed:
            self.anim_timer -= self.anim_speed
            self.anim_index = (self.anim_index + 1) % len(self.frames)
            self.base_image = self.frames[self.anim_index]

        now = pygame.time.get_ticks()

        run_away = False
        run_dir_x = 0.0
        run_dir_y = 0.0

        if isinstance(player, Carnivore):
            dx_p = player.rect.centerx - self.rect.centerx
            dy_p = player.rect.centery - self.rect.centery
            dist_p = math.hypot(dx_p, dy_p)
            if 0 < dist_p < self.fear_dist:
                run_away = True
                run_dir_x = -dx_p / dist_p
                run_dir_y = -dy_p / dist_p

        if run_away:
            angle = math.degrees(math.atan2(-run_dir_y, run_dir_x))
            current_frame = self.frames[self.anim_index]
            rotated = pygame.transform.rotate(current_frame, angle)
            old_center = self.rect.center
            self.image = rotated
            self.rect = self.image.get_rect(center=old_center)

            self.rect.x += run_dir_x * self.speed * dt * 0.8
            self.rect.y += run_dir_y * self.speed * dt * 0.8

        else:
            target = None
            min_dist = float("inf")
            for food in food_group:
                if isinstance(food, Plant):
                    dx = food.rect.centerx - self.rect.centerx
                    dy = food.rect.centery - self.rect.centery
                    dist = math.hypot(dx, dy)

                    if dist > self.seek_dist:
                        continue

                    if dist < min_dist:
                        min_dist = dist
                        target = food

            if target is not None:
                # ruch do jedzenia
                dx = target.rect.centerx - self.rect.centerx
                dy = target.rect.centery - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    dir_x = dx / dist
                    dir_y = dy / dist

                    # obrot
                    angle = math.degrees(math.atan2(-dir_y, dir_x))
                    current_frame = self.frames[self.anim_index]
                    rotated = pygame.transform.rotate(current_frame, angle)
                    old_center = self.rect.center
                    self.image = rotated
                    self.rect = self.image.get_rect(center=old_center)

                    self.rect.x += dir_x * self.speed * dt
                    self.rect.y += dir_y * self.speed * dt

            else:
                # wandering
                if now - self.wander_change_time > self.wander_interval:
                    self.wander_change_time = now
                    self.wander_dx, self.wander_dy = random_direction()

                dir_x = self.wander_dx
                dir_y = self.wander_dy

                # obrot
                angle = math.degrees(math.atan2(-dir_y, dir_x))
                current_frame = self.frames[self.anim_index]
                rotated = pygame.transform.rotate(current_frame, angle)
                old_center = self.rect.center
                self.image = rotated
                self.rect = self.image.get_rect(center=old_center)

                self.rect.x += dir_x * self.speed * dt * 0.8
                self.rect.y += dir_y * self.speed * dt * 0.8

        # zjadanie roslinek
        for food in list(food_group):
            if isinstance(food, Plant) and self.rect.colliderect(food.rect):
                food_group.remove(food)
                spawn_food_outside_view(game, Plant)
                break

        if self.has_level2_upgrade:
            now = pygame.time.get_ticks()
            if now - self.last_herb_attack >= self.herb_attack_cooldown:
                from game.Level_2.NPC_Herb_attack_logic import shoot_npc_herbivore
                if shoot_npc_herbivore(self, game):
                   self.last_herb_attack = now

        self.rect.clamp_ip(world_rect)