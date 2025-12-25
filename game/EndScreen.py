import pygame

class EndScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # background
        self.bgimage = pygame.image.load("visuals/background.png").convert()
        self.bgimage = pygame.transform.scale(self.bgimage, (self.width, self.height))

        # end
        self.end_image = pygame.image.load("visuals/The_End.png").convert_alpha()
        pw, ph = self.end_image.get_size()
        self.end_image = pygame.transform.smoothscale(self.end_image, (int(pw * 1.4), int(ph * 1.4)))

        # quit
        self.quit_image = pygame.image.load("visuals/quit_button.png").convert_alpha()
        qw, qh = self.quit_image.get_size()
        self.quit_image = pygame.transform.smoothscale(self.quit_image, (int(qw * 0.7), int(qh * 0.7)))

        self.end_rect = self.end_image.get_rect(center=(self.width // 2, self.height // 3 + 10))
        self.quit_rect = self.quit_image.get_rect(center=(self.width // 2, self.height // 2 + 10))

        self.next_state = "END"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.quit_rect.collidepoint(event.pos):
                    self.next_state = "QUIT"

    def update(self, dt):
        pass

    def draw(self):
        self.screen.blit(self.bgimage, (0, 0))
        self.screen.blit(self.end_image, self.end_rect)
        self.screen.blit(self.quit_image, self.quit_rect)