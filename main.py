import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


FPS = 60


def play():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.scr_width, settings.scr_height))
    pygame.display.set_caption('Alien Invasion')
    main_clock = pygame.time.Clock()

    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    # Make a ship
    ship = Ship(settings, screen)

    # Make bullets and aliens group
    bullets = Group()
    aliens = Group()
    gf.create_fleet(settings, screen, ship, aliens)

    # Make 'Play' button
    play_button = Button(screen, 'PLAY')

    # Set up music
    pygame.mixer.music.load('audio/background.mid')
    is_playing_music = False
    game_over_sound = pygame.mixer.Sound('audio/gameover.wav')

    # Main game loop
    game_over = False
    while not game_over:
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            if not is_playing_music:
                pygame.mixer.music.play(-1, 0.0)
                is_playing_music = True

            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(settings, screen, stats, sb, ship, aliens, bullets)
        else:
            if is_playing_music:
                pygame.mixer.music.stop()
                is_playing_music = False
                if stats.ships_left == 0:
                    game_over_sound.play()

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button)
        main_clock.tick(FPS)


play()
