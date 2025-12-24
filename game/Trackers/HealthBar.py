import pygame


class HealthBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_radius = 10

    def draw(self, surface, current_hp, max_hp):
        # border
        pygame.draw.rect(surface, (80, 80, 80),
                         (self.x, self.y, self.width, self.height),
                         width=2, border_radius=self.border_radius)


        # space between border and background
        padding = 2
        # background
        pygame.draw.rect(surface, (30, 30, 30),(self.x + padding, self.y + padding, self.width - 2 * padding, self.height - 2 * padding), border_radius=self.border_radius - 1)

        #bar fullness
        ratio = max(0, min(current_hp / max_hp, 1))
        fill_width = int((self.width - 2 * padding) * ratio)

        #color changes
        if ratio > 0.6:
            color = (60, 120, 60)
        elif ratio > 0.3:
            color = (150, 100, 30)
        else:
            color = (120, 40, 40)

        if fill_width > 0:
            pygame.draw.rect(surface, color,(self.x + padding, self.y + padding,fill_width, self.height - 2 * padding),border_radius=self.border_radius - 1)

        #hp text
        font = pygame.font.SysFont('georgia', 15)
        text = font.render(f"HP: {int(current_hp)}/{int(max_hp)}",True, (200, 200, 200))
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text, text_rect)
