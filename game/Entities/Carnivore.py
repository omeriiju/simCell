from .Entity import Entity
import pygame

class Carnivore(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "visuals/phase1/red_0.png")

        self.diet = "carnivore"

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

        self.original_image = self.frames[0]
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.rect.center)