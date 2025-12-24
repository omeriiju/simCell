import pygame

class ProgressBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_radius = 10

        self.level_thresholds = [20, 70, 150, 250]

    def draw(self, surface, current_xp, max_xp):
        # border
        pygame.draw.rect(surface, (80, 80, 80),
                         (self.x, self.y, self.width, self.height),
                         width=2, border_radius=self.border_radius)

        # space between border and background
        padding = 2
        # background
        pygame.draw.rect(surface, (30, 30, 30),
                         (self.x + padding, self.y + padding, self.width - 2 * padding, self.height - 2 * padding),
                         border_radius=self.border_radius - 1)

        ratio = max(0, min(current_xp / max_xp, 1))
        fill_width = int((self.width - 2 * padding) * ratio)

        if fill_width > 0:
            pygame.draw.rect(surface, (134,120,153),
                             (self.x + padding, self.y + padding, fill_width, self.height - 2 * padding),
                             border_radius=self.border_radius - 1)

        #lines indicating level-up
        inner_width = self.width - 2 * padding
        for threshold in self.level_thresholds[:-1]:  # Nie rysuj linii na końcu (250)
            threshold_ratio = threshold / max_xp
            line_x = self.x + padding + int(inner_width * threshold_ratio)

            pygame.draw.line(surface, (150, 150, 150),
                             (line_x, self.y + padding),
                             (line_x, self.y + self.height - padding),
                             2)

        font = pygame.font.SysFont('georgia', 17)
        text = font.render(f"XP: {int(current_xp)}/{max_xp}",True, (200, 200, 200))
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text, text_rect)