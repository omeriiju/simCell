import pygame

class SecondLevelUpgrade:
    def __init__(self, screen, player_diet):
        self.chosen_upgrade = None
        self.player_diet = player_diet

        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.bg_image = pygame.image.load("visuals/background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        self.top_image = pygame.image.load("visuals/phase2/one_upgrade_pick.png").convert_alpha()
        tiw, tih = self.top_image.get_size()
        scale = 1.65
        self.top_image = pygame.transform.smoothscale(self.top_image,(int(tiw * scale), int(tih * scale)))

        self.title_font = pygame.font.Font(None, 70)
        self.desc_font = pygame.font.Font(None, 28)

        frame_width = 450
        frame_height = 400
        spacing = 80

        left_x = (self.width // 2) - frame_width - (spacing // 2)
        frame_y = (self.height - frame_height) // 2 + 40
        self.left_rect = pygame.Rect(left_x, frame_y, frame_width, frame_height)

        right_x = (self.width // 2) + (spacing // 2)
        self.right_rect = pygame.Rect(right_x, frame_y, frame_width, frame_height)

        self.top_rect = self.top_image.get_rect(centerx=self.width // 2, top=-190)

        if player_diet == 'carnivore':
            left_image = pygame.image.load("visuals/phase2/red_hp_1.png").convert_alpha()
        else:
            left_image = pygame.image.load("visuals/phase2/green_hp_1.png").convert_alpha()
        max_width = int(frame_width * 0.4)
        orig_w, orig_h = left_image.get_size()
        scale_factor = max_width / orig_w
        new_h = int(orig_h * scale_factor)
        self.left_image = pygame.transform.smoothscale(left_image, (max_width, new_h))

        if player_diet == 'carnivore':
            right_image = pygame.image.load("visuals/phase2/red_dmg_1.png").convert_alpha()
        else:
            right_image = pygame.image.load("visuals/phase2/green_dmg_1.png").convert_alpha()
        orig_w, orig_h = right_image.get_size()
        scale_factor = max_width / orig_w
        new_h = int(orig_h * scale_factor)
        self.right_image = pygame.transform.smoothscale(right_image, (max_width, new_h))

        self.left_title = "Health"
        self.right_title = "Damage"
        self.left_desc = "Additional 150 hp."
        self.right_desc = "Your attacks are stronger.\nCarnivore: Deal 150 more damage.\nHerbivore: Deal 50 more damage"

        self.next_state = "SECOND_LVL_UPGRADE"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.left_rect.collidepoint(event.pos):
                    self.chosen_upgrade = "health"
                    self.next_state = "GAME"
                elif self.right_rect.collidepoint(event.pos):
                    self.chosen_upgrade = "damage"
                    self.next_state = "GAME"

    def update(self, dt):
        pass

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        self.screen.blit(self.top_image, self.top_rect)

        pygame.draw.rect(self.screen, (225, 255, 225), self.left_rect, 5)
        pygame.draw.rect(self.screen, (255, 210, 210), self.right_rect, 5)

        left_title_surf = self.title_font.render(self.left_title, True, (139, 192, 193))
        left_title_rect = left_title_surf.get_rect(centerx=self.left_rect.centerx, top=self.left_rect.top + 30)
        self.screen.blit(left_title_surf, left_title_rect)

        left_img_y = left_title_rect.bottom + 40
        left_img_rect = self.left_image.get_rect(centerx=self.left_rect.centerx, top=left_img_y)
        self.screen.blit(self.left_image, left_img_rect)

        y_offset = left_img_rect.bottom + 30
        for i, line in enumerate(self.left_desc.split("\n")):
            desc_surf = self.desc_font.render(line, True, (200, 200, 200))
            desc_rect = desc_surf.get_rect(centerx=self.left_rect.centerx, top=y_offset + i * 30)
            self.screen.blit(desc_surf, desc_rect)

        right_title_surf = self.title_font.render(self.right_title, True, (139, 192, 193))
        right_title_rect = right_title_surf.get_rect(centerx=self.right_rect.centerx, top=self.right_rect.top + 30)
        self.screen.blit(right_title_surf, right_title_rect)

        right_img_y = right_title_rect.bottom + 40
        right_img_rect = self.right_image.get_rect(centerx=self.right_rect.centerx, top=right_img_y)
        self.screen.blit(self.right_image, right_img_rect)

        y_offset = right_img_rect.bottom + 30
        for i, line in enumerate(self.right_desc.split("\n")):
            desc_surf = self.desc_font.render(line, True, (200, 200, 200))
            desc_rect = desc_surf.get_rect(centerx=self.right_rect.centerx, top=y_offset + i * 30)
            self.screen.blit(desc_surf, desc_rect)
