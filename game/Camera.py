import pygame
import random

def get_camera_rect(game):
    cam_x = game.player.rect.centerx - game.width // 2
    cam_y = game.player.rect.centery - game.height // 2
    cam_x = max(0, min(cam_x, game.map_width - game.width))
    cam_y = max(0, min(cam_y, game.map_height - game.height))
    return pygame.Rect(cam_x, cam_y, game.width, game.height)

def random_pos_outside_camera(game):
    camera_rect = get_camera_rect(game)
    while True:
        x = random.randint(0, game.map_width)
        y = random.randint(0, game.map_height)
        if not camera_rect.collidepoint(x, y):
            return x, y
