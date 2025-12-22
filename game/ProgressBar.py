import pygame

class ProgressBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, surface, current_xp, max_xp):
        pygame.draw.rect(surface, (30, 30, 30),
                         (self.x, self.y, self.width, self.height))

        ratio = max(0, min(current_xp / max_xp, 1))
        fill_width = int(self.width * ratio)
        pygame.draw.rect(surface, (0, 200, 0),
                         (self.x, self.y, fill_width, self.height))

        font = pygame.font.SysFont(None, 24)
        text = font.render(f"XP: {int(current_xp)}/{max_xp}",
                           True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        surface.blit(text, text_rect)