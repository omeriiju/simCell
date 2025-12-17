import pygame

from game.Entities.Carnivore import Carnivore
from game.Entities.Herbivore import Herbivore
import math


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # background
        self.bg_image = pygame.image.load("visuals/background.png").convert()
        zoom = 3.0
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

        #phase1
        self.all_sprites = pygame.sprite.Group()
        self.player = Carnivore(self.width // 2, self.height // 2)
        self.all_sprites.add(self.player)

        self.speed = 250

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

    def draw(self):
        cam_x = self.player.rect.centerx - self.width // 2
        cam_y = self.player.rect.centery - self.height // 2

        cam_x = max(0, min(cam_x, self.map_width - self.width))
        cam_y = max(0, min(cam_y, self.map_height - self.height))

        self.screen.blit(self.bg_image, (-cam_x, -cam_y))

        for sprite in self.all_sprites:
            draw_rect = sprite.rect.move(-cam_x, -cam_y)
            self.screen.blit(sprite.image, draw_rect)

        self.screen.blit(self.pause_button_image, self.pause_button_rect)