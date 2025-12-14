import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        #background
        self.bg_image = pygame.image.load("visuals/background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        #title
        self.title_image = pygame.image.load("visuals/title.png").convert_alpha()
        tw, th = self.title_image.get_size()
        self.title_image = pygame.transform.smoothscale(
            self.title_image,
            (int(tw * 1.3), int(th * 1.3))
        )

        #start button
        self.start_image = pygame.image.load("visuals/start_button.png").convert_alpha()
        bw, bh = self.start_image.get_size()
        self.start_image = pygame.transform.smoothscale(
            self.start_image,
            (int(bw * 0.7), int(bh * 0.7))
        )

        #quit button
        self.quit_image = pygame.image.load("visuals/quit_button.png").convert_alpha()
        qw, qh = self.quit_image.get_size()
        self.quit_image = pygame.transform.smoothscale(
            self.quit_image,
            (int(qw * 0.7), int(qh * 0.7))
        )

        self.title_rect = self.title_image.get_rect(center=(self.width // 2, self.height // 3))
        self.start_rect = self.start_image.get_rect(center=(self.width // 2, self.height // 3 + 150))
        self.quit_rect = self.quit_image.get_rect(center=(self.width // 2, self.height // 3 + 250))

        self.next_state = "MENU"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_rect.collidepoint(event.pos):
                    self.next_state = "GAME"
                if self.quit_rect.collidepoint(event.pos):
                    self.next_state = "QUIT"

    def update(self, dt):
        #animacje w menu?
        pass

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.screen.blit(self.title_image, self.title_rect)
        self.screen.blit(self.start_image, self.start_rect)
        self.screen.blit(self.quit_image, self.quit_rect)
