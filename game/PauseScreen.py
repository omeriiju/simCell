# PauseScreen.py
import pygame

class PauseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # background
        self.bgimage = pygame.image.load("visuals/background.png").convert()
        self.bgimage = pygame.transform.scale(self.bgimage, (self.width, self.height))

        # pause
        self.pause_image = pygame.image.load("visuals/pause.png").convert_alpha()
        pw, ph = self.pause_image.get_size()
        self.pause_image = pygame.transform.smoothscale(self.pause_image, (int(pw * 1.2), int(ph * 1.2)))

        # resume
        self.resume_image = pygame.image.load("visuals/resume.png").convert_alpha()
        rw, rh = self.resume_image.get_size()
        self.resume_image = pygame.transform.smoothscale(self.resume_image, (int(rw * 0.8), int(rh * 0.8)))

        # quit
        self.quit_image = pygame.image.load("visuals/quit_button.png").convert_alpha()
        qw, qh = self.quit_image.get_size()
        self.quit_image = pygame.transform.smoothscale(self.quit_image, (int(qw * 0.7), int(qh * 0.7)))

        self.pause_rect = self.pause_image.get_rect(center=(self.width // 2, self.height // 3 + 10))
        self.resume_rect = self.resume_image.get_rect(center=(self.width // 2, self.height // 2))
        self.quit_rect = self.quit_image.get_rect(center=(self.width // 2, self.height // 2 + 100))

        self.next_state = "PAUSE"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = "QUIT"

            # wznowienie gry
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.next_state = "GAME"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.resume_rect.collidepoint(event.pos):
                    self.next_state = "GAME"
                if self.quit_rect.collidepoint(event.pos):
                    self.next_state = "QUIT"

    def update(self, dt):
        pass

    def draw(self):
        self.screen.blit(self.bgimage, (0, 0))
        self.screen.blit(self.pause_image, self.pause_rect)
        self.screen.blit(self.resume_image, self.resume_rect)
        self.screen.blit(self.quit_image, self.quit_rect)
