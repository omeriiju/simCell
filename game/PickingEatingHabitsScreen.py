import pygame


class PickingEatingHabitsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        # background
        self.bg_image = pygame.image.load("visuals/background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.width, self.height))

        # pick
        self.pick_image = pygame.image.load("visuals/pick_side.png").convert_alpha()
        pcw, pch = self.pick_image.get_size()
        self.pick_image = pygame.transform.smoothscale(self.pick_image, (int(pcw * 1.3), int(pch * 1.3)))

        # font
        self.title_font = pygame.font.Font(None, 70)
        self.desc_font = pygame.font.Font(None, 28)

        # frame
        frame_width = 450
        frame_height = 500
        spacing = 80

        # left frame (Herbivore)
        left_x = (self.width // 2) - frame_width - (spacing // 2)
        frame_y = (self.height - frame_height) // 2 + 60
        self.herbivore_rect = pygame.Rect(left_x, frame_y, frame_width, frame_height)

        # right frame (Carnivore)
        right_x = (self.width // 2) + (spacing // 2)
        self.carnivore_rect = pygame.Rect(right_x, frame_y, frame_width, frame_height)

        # pick
        self.pick_rect = self.pick_image.get_rect(centerx=self.width // 2, bottom=frame_y - 5)

        herbivore_image = pygame.image.load("visuals/phase1/green_1.png").convert_alpha()
        max_width = 350
        orig_w, orig_h = herbivore_image.get_size()
        scale_factor = max_width / orig_w
        new_h = int(orig_h * scale_factor)
        self.herbivore_image = pygame.transform.smoothscale(herbivore_image, (max_width, new_h))

        carnivore_image = pygame.image.load("visuals/phase1/red_1.png").convert_alpha()
        max_width = 350
        orig_w, orig_h = carnivore_image.get_size()
        scale_factor = max_width / orig_w
        new_h = int(orig_h * scale_factor)
        self.carnivore_image = pygame.transform.smoothscale(carnivore_image, (max_width, new_h))

        # descriptions
        self.herbivore_desc = "Eats plants and vegetation.\nPeaceful nature."
        self.carnivore_desc = "Hunts other organisms.\nAggressive towards others."

        self.next_state = "PICKING"
        self.selected_type = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.herbivore_rect.collidepoint(event.pos):
                    self.selected_type = "Herbivore"
                    self.next_state = "GAME"
                elif self.carnivore_rect.collidepoint(event.pos):
                    self.selected_type = "Carnivore"
                    self.next_state = "GAME"

    def update(self, dt):
        pass

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        self.screen.blit(self.pick_image, self.pick_rect)

        # frames
        pygame.draw.rect(self.screen, (225, 255, 225), self.herbivore_rect, 5, border_radius=10)
        pygame.draw.rect(self.screen, (255, 210, 210), self.carnivore_rect, 5, border_radius=10)

        # Herbivore frame
        herb_title = self.title_font.render("Herbivore", True, (139, 192, 193))
        herb_title_rect = herb_title.get_rect(centerx=self.herbivore_rect.centerx, top=self.herbivore_rect.top + 30)
        self.screen.blit(herb_title, herb_title_rect)

        # picture
        herb_img_y = herb_title_rect.bottom + 40
        herb_img_rect = self.herbivore_image.get_rect(centerx=self.herbivore_rect.centerx, top=herb_img_y)
        self.screen.blit(self.herbivore_image, herb_img_rect)

        # description
        y_offset = herb_img_rect.bottom + 30
        for i, line in enumerate(self.herbivore_desc.split('\n')):
            desc_surf = self.desc_font.render(line, True, (200, 200, 200))
            desc_rect = desc_surf.get_rect(centerx=self.herbivore_rect.centerx, top=y_offset + i * 30)
            self.screen.blit(desc_surf, desc_rect)

        # Carnivore frame
        carn_title = self.title_font.render("Carnivore", True, (139, 192, 193))
        carn_title_rect = carn_title.get_rect(centerx=self.carnivore_rect.centerx, top=self.carnivore_rect.top + 30)
        self.screen.blit(carn_title, carn_title_rect)

        # picture
        carn_img_y = carn_title_rect.bottom + 40
        carn_img_rect = self.carnivore_image.get_rect(centerx=self.carnivore_rect.centerx,
                                                      top=carn_img_y)
        self.screen.blit(self.carnivore_image, carn_img_rect)

        # description
        y_offset = carn_img_rect.bottom + 30
        for i, line in enumerate(self.carnivore_desc.split('\n')):
            desc_surf = self.desc_font.render(line, True, (200, 200, 200))
            desc_rect = desc_surf.get_rect(centerx=self.carnivore_rect.centerx,
                                           top=y_offset + i * 30)
            self.screen.blit(desc_surf, desc_rect)