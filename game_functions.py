import sys
import pygame
from pygame.locals import *
from bullet import Bullet
from alien import Alien
from time import sleep


RIGHT_KEYS = [K_d, K_RIGHT]
LEFT_KEYS = [K_a, K_LEFT]


def change_fleet_direction(game_settings, aliens):
    """ Drop the fleet and change direction"""
    for a in aliens.sprites():
        a.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def check_fleet_edeges(game_settings, aliens):
    for a in aliens.sprites():
        if a.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def check_events(game_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets):
    """Respong to keypresses and mouse events."""
    for e in pygame.event.get():
        if e.type == QUIT:
            terminate()
        elif e.type == KEYDOWN:
            check_keydown_events(e, game_settings, screen, stats, ship, bullets)
        elif e.type == KEYUP:
            check_keyup_events(e, ship)
        elif e.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, scoreboard, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(game_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        game_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()

        # Clear aliens, bullets lists
        aliens.empty()
        bullets.empty()

        # Create aliens fleet and center the ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, game_settings, screen, stats, ship, bullets):
    """Respond to key presses"""
    if event.key in RIGHT_KEYS:
        ship.move_right = True
    elif event.key in LEFT_KEYS:
        ship.move_left = True
    elif event.key == K_SPACE:
        if stats.game_active:
            fire_bullet(game_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == K_ESCAPE or event.key == K_q:
        terminate()
    elif event.key in RIGHT_KEYS:
        ship.move_right = False
    elif event.key in LEFT_KEYS:
        ship.move_left = False


def check_aliens_bottom(game_settings, screen, stats, scoreboard, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for a in aliens.sprites():
        if a.rect.bottom >= screen_rect.height:
            ship_hit(game_settings, screen, stats, scoreboard, ship, aliens, bullets)
            break


def check_bullet_alien_collision(game_settings, screen, stats, scoreboard, ship, aliens, bullets):
    # Check for collision with aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
        scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        bullets.empty()
        game_settings.increase_speed()
        stats.level += 1
        scoreboard.prep_level()
        create_fleet(game_settings, screen, ship, aliens)
        sleep(0.75)


def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
    scoreboard.prep_high_score()


def create_alien(game_settings, screen, aliens, alien_number, row_number):
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(game_settings, screen, ship, aliens):
    """Create a fleet of aliens"""
    # Create an alien and find the number of aliens on a row
    # Spacing between each alien is equal to 1 alien width
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Create 1st row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def fire_bullet(game_settings, screen, ship, bullets):
    # Create a bullet and add to bullets group
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(game_settings, alien_width):
    available_space_x = game_settings.scr_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def get_number_rows(game_settings, ship_height, alien_height):
    available_space_y = (game_settings.scr_height - (3*alien_height) - ship_height)
    return int(available_space_y / (2*alien_height))


def ship_hit(game_settings, screen, stats, scoreboard, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        scoreboard.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.75)

    else:
        aliens.empty()
        bullets.empty()
        stats.game_active = False
        pygame.mouse.set_visible(True)


def terminate():
    pygame.quit()
    sys.exit()


def update_bullets(game_settings, screen, stats, scoreboard, ship, aliens, bullets):
    bullets.update()
    check_bullet_alien_collision(game_settings, screen, stats, scoreboard, ship, aliens, bullets)

    # Delete out of screen bullets
    for b in bullets.copy():
        if b.rect.bottom <= 0:
            bullets.remove(b)
    # print(len(bullets))


def update_aliens(game_settings, screen, stats, scoreboard, ship, aliens, bullets):
    check_fleet_edeges(game_settings, aliens)
    aliens.update()
    check_aliens_bottom(game_settings, screen, stats, scoreboard, ship, aliens, bullets)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, screen, stats, scoreboard, ship, aliens, bullets)


def update_screen(game_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button):
    """Redraw the screen"""
    screen.fill(game_settings.bg_color)
    for b in bullets.sprites():
        b.draw()
    ship.draw()
    aliens.draw(screen)

    # Draw score
    scoreboard.draw()

    # Draw Play button
    if not stats.game_active:
        play_button.draw()

    pygame.display.update()
