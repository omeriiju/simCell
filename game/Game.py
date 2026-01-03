import pygame

from game.Entities.Carnivore import Carnivore
from game.Entities.Herbivore import Herbivore
import math

from game.GameLogic.Food import Plant, Meat
from game.GameLogic.Food_spawner import spawn_food_outside_view

from game.Entities.NPCHerbivore import NPCHerbivore
from game.Entities.NPCCarnivore import NPCCarnivore

from game.GameLogic.XP import add_xp
from game.GameLogic.NPC_spawner import spawn_npc_outside_view

import random

from game.Level_2.Level_2_Spawner_Carn import spawn_level2_carnivores
from game.Level_2.Level_2_Spawner_Herb import spawn_level2_herbivores
from game.Trackers.HealthBar import HealthBar
from game.Trackers.ProgressBar import ProgressBar

from game.Level_2.Herb_attack_logic import shoot_herbivore


def food_collision(player, food):
    return player.rect.colliderect(food.hitbox)

class Game:
    def __init__(self, screen, player_type="Carnivore"):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        #visuals ===============================================
        # background
        self.bg_image = pygame.image.load("visuals/background_2.png").convert()
        zoom = 5.0
        w, h = self.bg_image.get_size()
        self.bg_image = pygame.transform.smoothscale(self.bg_image,(int(w * zoom), int(h * zoom)))
        self.map_width, self.map_height = self.bg_image.get_size()
        self.world_rect = pygame.Rect(0, 0, self.map_width, self.map_height)

        # pause button
        self.pause_button_image = pygame.image.load("visuals/pause_button.png").convert_alpha()
        pbw, pbh = self.pause_button_image.get_size()
        self.pause_button_image = pygame.transform.smoothscale(self.pause_button_image, (int(pbw * 0.3), int(pbh * 0.3)))
        self.pause_button_rect = self.pause_button_image.get_rect(topleft=(20, 20))

        self.next_state = "GAME"
        #========================================================

        # player variant
        self.all_sprites = pygame.sprite.Group()

        self.npc_group = pygame.sprite.Group()

        # jedzenie
        self.food_group = pygame.sprite.Group()

        spawn_x = random.randint(0, self.map_width)
        spawn_y = random.randint(0, self.map_height)

        if player_type == "Herbivore":
            self.player = Herbivore(spawn_x, spawn_y)
        else:
            self.player = Carnivore(spawn_x, spawn_y)

        self.all_sprites.add(self.player)

        for _ in range(50):
            spawn_food_outside_view(self, Plant)

        for _ in range(50):
            spawn_food_outside_view(self, Meat)

        self.speed = 250

        #NPCs spawn
        for _ in range(25):
            spawn_npc_outside_view(self)

        for _ in range(25):
            spawn_npc_outside_view(self, NPCCarnivore)


        self.attack_cooldown = 300
        self.last_attack_time = 0
        self.knockback = 50

        #========================================================
        #progess bar
        bar_width = self.width - 40
        bar_height = 20
        bar_x = 20
        bar_y = self.height - bar_height - 20
        self.xp_bar = ProgressBar(bar_x, bar_y, bar_width, bar_height)

        #hp
        hp_bar_width = 400
        hp_bar_height = 20
        hp_bar_x = self.width - hp_bar_width - 20
        hp_bar_y = 20
        self.hp_bar = HealthBar(hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height)

        # lvl visuals
        self.current_level = 1
        self.level_up_show = False
        self.level_up_start_time = 0
        self.level_up_duration = 1500

        self.lvl_images = {
            1: pygame.image.load("visuals/level_1.png").convert_alpha(),
            2: pygame.image.load("visuals/level_2.png").convert_alpha(),
            3: pygame.image.load("visuals/level_3.png").convert_alpha(),
            4: pygame.image.load("visuals/level_4.png").convert_alpha(),
        }

        #lvl 1 at the beginning
        self.lvl1_show = True
        self.lvl1_start_time = pygame.time.get_ticks()
        self.lvl1_duration = 1500
        # ========================================================

        #herb attack
        self.herb_attack_damage = 30
        self.projectiles = pygame.sprite.Group()
        self.herb_attack_unlocked = False
        self.herb_attack_cooldown = 1250
        self.herb_attack_last = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.next_state = "PAUSE"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pause_button_rect.collidepoint(event.pos):
                    self.next_state = "PAUSE"

    def update(self, dt):
        if self.level_up_show:
            now = pygame.time.get_ticks()
            if now - self.level_up_start_time >= self.level_up_duration:
                self.level_up_show = False

        if self.lvl1_show:
            now = pygame.time.get_ticks()
            if now - self.lvl1_start_time >= self.lvl1_duration:
                self.lvl1_show = False

        keys = pygame.key.get_pressed()
        self.player.vx = 0
        self.player.vy = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.vx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.vx = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.vy = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.vy = 1

        # ruch w kazdym wymiarze ma stala predkosc
        length = math.hypot(self.player.vx, self.player.vy)
        if length != 0:
            self.player.vx = self.player.vx / length * self.speed
            self.player.vy = self.player.vy / length * self.speed
        else:
            self.player.vx = 0
            self.player.vy = 0

        self.player.update(dt)

        for sprite in self.all_sprites:
            if isinstance(sprite, NPCHerbivore):
                sprite.update(dt, self.food_group, self.world_rect, self.player, self)
            elif isinstance(sprite, NPCCarnivore):
                sprite.update(dt, self.food_group, self.world_rect, self.player, self.npc_group, self)
            elif sprite is not self.player:
                sprite.update(dt)

        self.player.rect.clamp_ip(self.world_rect)

        hits = pygame.sprite.spritecollide(
            self.player, self.food_group, dokill=False, collided=food_collision)

        for food in hits:
            if food.allowed_diet == self.player.diet:
                add_xp(self, 1)

                if self.player.health < self.player.max_health:
                    self.player.health = min(self.player.health + 10,self.player.max_health)

                food_type = type(food)
                self.food_group.remove(food)
                spawn_food_outside_view(self, food_type)

        now = pygame.time.get_ticks()

        for npc_carn in list(self.npc_group):
            if not isinstance(npc_carn, NPCCarnivore):
                continue

            if now - npc_carn.last_attack_time < npc_carn.attack_cooldown:
                continue

            victims = []

            for npc in self.npc_group:
                if isinstance(npc, NPCHerbivore):
                    victims.append(npc)

            npc_hitbox = npc_carn.rect.inflate(
                -npc_carn.rect.width * 0.1,
                -npc_carn.rect.height * 0.1
            )

            for victim in victims:
                victim_hitbox = victim.rect.inflate(
                    -victim.rect.width * 0.1,
                    -victim.rect.height * 0.1
                )

                if npc_hitbox.colliderect(victim_hitbox):
                    if hasattr(victim, "health") and victim.health > 0:
                        npc_carn.last_attack_time = now
                        victim.health -= npc_carn.attack_damage

                        dx = victim.rect.centerx - npc_carn.rect.centerx
                        dy = victim.rect.centery - npc_carn.rect.centery
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            dx /= dist
                            dy /= dist
                            victim.rect.x += dx * self.knockback
                            victim.rect.y += dy * self.knockback
                            victim.rect.clamp_ip(self.world_rect)

                        if isinstance(victim, NPCHerbivore) and victim.health <= 0:
                            self.npc_group.remove(victim)
                            self.all_sprites.remove(victim)
                            if isinstance(victim, NPCHerbivore):
                                if getattr(victim, "has_level2_upgrade", False):
                                    spawn_level2_herbivores(self, 1)
                                else:
                                    spawn_npc_outside_view(self)
                            else:
                                if getattr(victim, "has_level2_upgrade", False):
                                    spawn_level2_carnivores(self, 1)
                                else:
                                    spawn_npc_outside_view(self, NPCCarnivore)
                    break

        now = pygame.time.get_ticks()

        player_hitbox = self.player.rect.inflate(
            -self.player.rect.width * 0.1,
            -self.player.rect.height * 0.1
        )

        bite_targets = []
        biting_carnivores = []

        for npc in self.npc_group:
            npc_hitbox = npc.rect.inflate(
                -npc.rect.width * 0.1,
                -npc.rect.height * 0.1
            )
            if player_hitbox.colliderect(npc_hitbox):
                if hasattr(npc, "health") and npc.health > 0:
                    bite_targets.append(npc)
                if isinstance(npc, NPCCarnivore):
                    biting_carnivores.append(npc)

        can_player_bite = (
                isinstance(self.player, Carnivore) and
                now - self.last_attack_time >= self.attack_cooldown and
                len(bite_targets) > 0
        )

        can_npc_bite = any(
            now - npc.last_attack_time >= npc.attack_cooldown
            for npc in biting_carnivores
        )

        if can_player_bite:
            self.last_attack_time = now
            enemy = bite_targets[0]
            if hasattr(enemy, "health") and enemy.health > 0:
                enemy.health -= self.player.attack_damage

                dx = enemy.rect.centerx - self.player.rect.centerx
                dy = enemy.rect.centery - self.player.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    dx /= dist
                    dy /= dist
                    enemy.rect.x += dx * self.knockback
                    enemy.rect.y += dy * self.knockback
                    enemy.rect.clamp_ip(self.world_rect)

                if enemy.health <= 0:
                    add_xp(self, 3)
                    self.npc_group.remove(enemy)
                    self.all_sprites.remove(enemy)

                    if isinstance(enemy, NPCHerbivore):
                        if getattr(enemy, "has_level2_upgrade", False):
                            spawn_level2_herbivores(self, 1)
                        else:
                            spawn_npc_outside_view(self)
                    else:
                        if getattr(enemy, "has_level2_upgrade", False):
                            spawn_level2_carnivores(self, 1)
                        else:
                            spawn_npc_outside_view(self, NPCCarnivore)

        elif can_npc_bite:
            npc = next(n for n in biting_carnivores if now - n.last_attack_time >= n.attack_cooldown)
            npc.last_attack_time = now
            if self.player.health > 0:
                self.player.health -= npc.attack_damage

                dx = self.player.rect.centerx - npc.rect.centerx
                dy = self.player.rect.centery - npc.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    dx /= dist
                    dy /= dist
                    self.player.rect.x += dx * self.knockback
                    self.player.rect.y += dy * self.knockback
                    self.player.rect.clamp_ip(self.world_rect)

                if self.player.health <= 0:
                    self.next_state = "END"

        #herb attack
        self.projectiles.update(dt, self.world_rect)
        shoot_herbivore(self)

        for proj in list(self.projectiles):
            if getattr(proj, "owner", None) == "npc":
                continue

            hits = pygame.sprite.spritecollide(proj, self.npc_group, dokill=False)
            for npc in hits:
                if hasattr(npc, "health") and npc.health > 0:
                    npc.health -= proj.damage
                    if npc.health <= 0:
                        self.npc_group.remove(npc)
                        self.all_sprites.remove(npc)

                        if getattr(proj, "owner", None) == "player":
                            add_xp(self, 3)

                        if isinstance(npc, NPCHerbivore):
                            if getattr(npc, "has_level2_upgrade", False):
                                spawn_level2_herbivores(self, 1)
                            else:
                                spawn_npc_outside_view(self)
                        else:
                            if getattr(npc, "has_level2_upgrade", False):
                                spawn_level2_carnivores(self, 1)
                            else:
                                spawn_npc_outside_view(self, NPCCarnivore)
                proj.kill()
                break

        for proj in list(self.projectiles):
            if getattr(proj, "owner", None) == "npc":
                if self.player.rect.colliderect(proj.rect):
                    if self.player.health > 0:
                        self.player.health -= proj.damage

                        if self.player.health <= 0:
                            self.next_state = "END"

                    proj.kill()


    def draw(self):
        cam_x = self.player.rect.centerx - self.width // 2
        cam_y = self.player.rect.centery - self.height // 2

        cam_x = max(0, min(cam_x, self.map_width - self.width))
        cam_y = max(0, min(cam_y, self.map_height - self.height))

        self.screen.blit(self.bg_image, (-cam_x, -cam_y))

        for food in self.food_group:
            draw_rect = food.rect.move(-cam_x, -cam_y)
            self.screen.blit(food.image, draw_rect)

        for sprite in self.all_sprites:
            draw_rect = sprite.rect.move(-cam_x, -cam_y)
            self.screen.blit(sprite.image, draw_rect)

        self.screen.blit(self.pause_button_image, self.pause_button_rect)

        self.xp_bar.draw(self.screen, self.player.xp, self.player.max_xp)

        self.hp_bar.draw(self.screen, self.player.health, self.player.max_health)

        if self.lvl1_show:
            lvl_rect = self.lvl_images[1].get_rect(center=(self.width // 2, self.height // 2 - 200))
            self.screen.blit(self.lvl_images[1], lvl_rect)

        if self.level_up_show and self.current_level in self.lvl_images:
            lvl_rect = self.lvl_images[self.current_level].get_rect(center=(self.width // 2, self.height // 2 - 200))
            self.screen.blit(self.lvl_images[self.current_level], lvl_rect)

        # current lvl
        font = pygame.font.SysFont('georgia', 20, bold=True)
        level_text = font.render(f"Level {self.player.get_level()}", True, (200, 200, 200))
        level_rect = level_text.get_rect(topleft=(20, self.height - 70))
        self.screen.blit(level_text, level_rect)

        for proj in self.projectiles:
            draw_rect = proj.rect.move(-cam_x, -cam_y)
            self.screen.blit(proj.image, draw_rect)