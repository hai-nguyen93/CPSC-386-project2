import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets"""
    def __init__(self, game_settings, screen, ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, game_settings.bullet_width, game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top

        self.y = float(self.rect.top)

        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed_factor

    def update(self):
        """Move the bullet"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
