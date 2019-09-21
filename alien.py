import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, game_settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = game_settings

        # load image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # starting position near top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.settings.fleet_direction * self.settings.alien_speed_factor)
        self.rect.x = self.x
