import pygame
import math

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        original_image = pygame.image.load(image_path).convert_alpha()

        #przeskalowanie postaci
        scale = 0.2
        w, h = original_image.get_size()
        self.original_image = pygame.transform.smoothscale(
            original_image,
            (int(w * scale), int(h * scale))
        )

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 0
        self.vy = 0
        self.angle = 0

        #animacja
        self.frames = None
        self.anim_index = 0
        self.anim_timer = 0.0
        #sekundy na klatke
        self.anim_speed = 0.2

        #eating habits + xp
        self.xp = 0
        self.diet = None
        self.max_xp = 250
        self.level = 1

        #health
        self.health = 200
        self.max_health = 200
        self.attack_damage = 100

    def get_level(self):
        if self.xp >= 250:
            #the end
            return 5
        elif self.xp >= 150:
            return 4
        elif self.xp >= 70:
            return 3
        elif self.xp >= 1:
            return 2
        else:
            #begining of the game
            return 1


    def update(self, dt):
        #animacja
        if self.frames is not None:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer -= self.anim_speed
                self.anim_index = (self.anim_index + 1) % len(self.frames)
                self.original_image = self.frames[self.anim_index]

        #ruch
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt

        #obrot
        if self.vx != 0 or self.vy != 0:
            target_angle = math.degrees(math.atan2(self.vy, self.vx))
            diff = (target_angle - self.angle + 180) % 360 - 180

            rotate_speed = 500

            max_step = rotate_speed * dt

            if diff > max_step:
                diff = max_step
            elif diff < -max_step:
                diff = -max_step

            self.angle += diff

        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        old_center = self.rect.center
        self.image = rotated_image
        self.rect = self.image.get_rect(center=old_center)

