import pygame


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, allowed_diet):
        super().__init__()
        img = pygame.image.load(image_path).convert_alpha()
        scale = 0.08
        w, h = img.get_size()
        self.image = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))

        self.rect = self.image.get_rect(center=(x, y))

        #zmniejszenie hitboxu
        hit_w = int(self.rect.width * 0.2)
        hit_h = int(self.rect.height * 0.2)
        self.hitbox = pygame.Rect(0, 0, hit_w, hit_h)
        self.hitbox.center = self.rect.center

        self.allowed_diet = allowed_diet

    def update(self, dt):
        self.hitbox.center = self.rect.center

class Plant(Food):
    def __init__(self, x, y):
        super().__init__(x, y, "visuals/food/roslinka_blender.png", "herbivore")


class Meat(Food):
    def __init__(self, x, y):
        super().__init__(x, y, "visuals/food/miesko_blender.png", "carnivore")
