import pygame

from game.Entities.Carnivore import Carnivore
from game.Entities.Herbivore import Herbivore
import math
from game.GameLogic.Food import Plant, Meat
import random

from game.Trackers.HealthBar import HealthBar
from game.Trackers.ProgressBar import ProgressBar

def food_collision(player, food):
    return player.rect.colliderect(food.hitbox)

class Game:
    def __init__(self, screen, player_type="Carnivore"):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

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

        # player variant
        self.all_sprites = pygame.sprite.Group()
        # jedzenie
        self.food_group = pygame.sprite.Group()

        spawn_x = random.randint(0, self.map_width)
        spawn_y = random.randint(0, self.map_height)

        if player_type == "Herbivore":
            self.player = Herbivore(spawn_x, spawn_y)
        else:
            self.player = Carnivore(spawn_x, spawn_y)

        self.all_sprites.add(self.player)

        for _ in range(30):
            self.spawn_food_outside_view()

        self.speed = 250

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

    def get_camera_rect(self):
        cam_x = self.player.rect.centerx - self.width // 2
        cam_y = self.player.rect.centery - self.height // 2
        cam_x = max(0, min(cam_x, self.map_width - self.width))
        cam_y = max(0, min(cam_y, self.map_height - self.height))
        return pygame.Rect(cam_x, cam_y, self.width, self.height)

    def random_pos_outside_camera(self):
        camera_rect = self.get_camera_rect()
        while True:
            x = random.randint(0, self.map_width)
            y = random.randint(0, self.map_height)
            if not camera_rect.collidepoint(x, y):
                return x, y

    def spawn_food_outside_view(self):
        x, y = self.random_pos_outside_camera()
        if random.random() < 0.5:
            food = Plant(x, y)
        else:
            food = Meat(x, y)
        self.food_group.add(food)

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

        self.all_sprites.update(dt)
        self.player.rect.clamp_ip(self.world_rect)

        hits = pygame.sprite.spritecollide(
            self.player, self.food_group, dokill=False, collided=food_collision)

        for food in hits:
            if food.allowed_diet == self.player.diet:
                old_level = self.player.get_level()
                self.player.xp += 1
                new_level = self.player.get_level()

                # is new level acquired
                if new_level > old_level:
                    self.current_level = new_level
                    self.level_up_show = True
                    self.level_up_start_time = pygame.time.get_ticks()

                    # hp increase
                    self.player.max_health += 50
                    self.player.health += 50

                if new_level == 5:
                    self.next_state = "END"

                food_type = type(food)
                self.food_group.remove(food)

                x, y = self.random_pos_outside_camera()
                new_food = food_type(x, y)
                self.food_group.add(new_food)

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