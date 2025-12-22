import pygame
from MainMenu import MainMenu
from Game import Game
from PauseScreen import PauseScreen
from PickingEatingHabitsScreen import PickingEatingHabitsScreen

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
        elif state.next_state == "PAUSE" and isinstance(state, Game):
            previous_state = state
            state = PauseScreen(screen)
        #powrot po pauzie
        elif state.next_state == "GAME" and isinstance(state, PauseScreen):
            state = previous_state
            state.next_state = "GAME"
        elif state.next_state == "QUIT":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()