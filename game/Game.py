import pygame

from game.Entities.Carnivore import Carnivore
from game.Entities.Herbivore import Herbivore


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # background
        self.bg_image = pygame.image.load("visuals/background.png").convert()
        zoom = 3.0
        w, h = self.bg_image.get_size()
        self.bg_image = pygame.transform.smoothscale(
            self.bg_image,
            (int(w * zoom), int(h * zoom))
        )
        self.map_width, self.map_height = self.bg_image.get_size()
        self.world_rect = pygame.Rect(0, 0, self.map_width, self.map_height)

        self.next_state = "GAME"

        #phase1
        self.all_sprites = pygame.sprite.Group()
        self.player = Herbivore(self.width // 2, self.height // 2)
        self.all_sprites.add(self.player)

        self.speed = 250


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = "QUIT"

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.vx = 0
        self.player.vy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.vx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.vx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.vy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.vy = self.speed

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