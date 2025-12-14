import pygame
from MainMenu import MainMenu
from Game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("simCell")
    clock = pygame.time.Clock()

    state = MainMenu(screen)
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

        if state.next_state == "GAME" and isinstance(state, MainMenu):
            state = Game(screen)
        elif state.next_state == "MENU" and isinstance(state, Game):
            state = MainMenu(screen)
        elif state.next_state == "QUIT":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()