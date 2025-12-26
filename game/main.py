import pygame
from MainMenu import MainMenu
from Game import Game
from PauseScreen import PauseScreen
from PickingEatingHabitsScreen import PickingEatingHabitsScreen
from EndScreen import EndScreen
from game.Level_2.SecondLevelUpgrade import SecondLevelUpgrade


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("simCell")
    clock = pygame.time.Clock()

    state = MainMenu(screen)
    previous_state = None
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        state.handle_events(events)
        state.update(dt)
        state.draw()
        pygame.display.flip()

        if state.next_state == "PICKING" and isinstance(state, MainMenu):
            state = PickingEatingHabitsScreen(screen)
        elif state.next_state == "GAME" and isinstance(state, PickingEatingHabitsScreen):
            state = Game(screen, state.selected_type)
        elif state.next_state == "MENU" and isinstance(state, Game):
            state = MainMenu(screen)

        #pauza
        elif state.next_state == "PAUSE" and isinstance(state, Game):
            previous_state = state
            state = PauseScreen(screen)
        #powrot po pauzie
        elif state.next_state == "GAME" and isinstance(state, PauseScreen):
            state = previous_state
            state.next_state = "GAME"

        elif state.next_state == "END" and isinstance(state, Game):
            state = EndScreen(screen)

        #upgrade 1 i powrot do gry
        elif state.next_state == "SECOND_LVL_UPGRADE" and isinstance(state, Game):
            previous_state = state
            state = SecondLevelUpgrade(screen, previous_state.player.diet)
        elif state.next_state == "GAME" and isinstance(state, SecondLevelUpgrade):
            if state.chosen_upgrade == "health":
                previous_state.player.max_health += 150
                previous_state.player.health += 150

                new_frames = []
                scale = 0.1

                if previous_state.player.diet == "herbivore":
                    base_path = "visuals/phase2/green_hp_"
                else:
                    base_path = "visuals/phase2/red_hp_"

                for i in range(2):
                    img = pygame.image.load(f"{base_path}{i}.png").convert_alpha()
                    w, h = img.get_size()
                    img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
                    new_frames.append(img)

                previous_state.player.frames = new_frames
                previous_state.player.anim_index = 0
                previous_state.player.anim_timer = 0.0
                previous_state.player.anim_speed = 0.25
                previous_state.player.original_image = previous_state.player.frames[0]

                old_center = previous_state.player.rect.center
                previous_state.player.image = previous_state.player.original_image
                previous_state.player.rect = previous_state.player.image.get_rect(center=old_center)

            elif state.chosen_upgrade == "damage":
                previous_state.player.attack_damage += 150
                previous_state.herb_attack_damage += 50

                new_frames = []
                scale = 0.1

                if previous_state.player.diet == "herbivore":
                    base_path = "visuals/phase2/green_dmg_"
                else:
                    base_path = "visuals/phase2/red_dmg_"

                for i in range(2):
                    img = pygame.image.load(f"{base_path}{i}.png").convert_alpha()
                    w, h = img.get_size()
                    img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
                    new_frames.append(img)

                previous_state.player.frames = new_frames
                previous_state.player.anim_index = 0
                previous_state.player.anim_timer = 0.0
                previous_state.player.anim_speed = 0.25
                previous_state.player.original_image = previous_state.player.frames[0]

                old_center = previous_state.player.rect.center
                previous_state.player.image = previous_state.player.original_image
                previous_state.player.rect = previous_state.player.image.get_rect(center=old_center)

            previous_state.current_level = 2
            previous_state.level_up_show = True
            previous_state.level_up_start_time = pygame.time.get_ticks()

            state = previous_state
            state.next_state = "GAME"

        elif state.next_state == "QUIT":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()