import pygame

class HerbAttack(pygame.sprite.Sprite):
    def __init__(self, pos, vel, damage, max_range, groups):
        super().__init__(*groups)

        self.damage = damage

        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.damage = damage
        self.max_range = max_range
        self.start_pos = self.pos.copy()

        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.image.fill((120, 255, 120))
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt, world_rect):
        # ruch
        self.pos += self.vel * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if self.start_pos.distance_to(self.pos) >= self.max_range:
            self.kill()
            return

        if not world_rect.colliderect(self.rect):
            self.kill()