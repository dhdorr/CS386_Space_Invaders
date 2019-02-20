import sys
from time import sleep

import pygame
import random

from bullet import Bullet, Alien_Bullet
from alien import Alien
from Alien2 import Alien2
from Alien3 import Alien3
from bunker import Bunker
from alienUFO import AlienUFO


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    shoot_effect = pygame.mixer.Sound('songs/shoot.wav')
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        shoot_effect.play()
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, bunkers, ufos, alien_bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            final_score = stats.score
            file = open("high_score.txt", "w")
            file.write("High Scores!\n")
            file.write(str(final_score))
            file.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, mouse_x, mouse_y, bunkers, ufos)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
        aliens, bullets, mouse_x, mouse_y, bunkers, ufos):
    pygame.mixer.music.load("songs/bg_music2.mp3")
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        pygame.mixer.music.play(-1, 0.0)

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        bunkers.empty()
        #ufos.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        create_bunkers(ai_settings, screen, ship, bunkers)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def alien_fire_bullet(ai_settings, screen, aliens, alien_bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new alien bullet, add to bullets group.
    new_bullet = Alien_Bullet(ai_settings, screen, aliens)
    alien_bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button, bunkers, ufos, alien_bullets):
    alien_shot = pygame.mixer.Sound('songs/alien_shoot.wav')

    """Update images on the screen, and flip to the new screen."""
    alien_shoot = random.randint(1,201)
    rare_ufo = random.randint(1,3000)
    if alien_shoot > 10 and alien_shoot < 15:
        alien_fire_bullet(ai_settings, screen, aliens, alien_bullets)
        alien_shot.play()


    if rare_ufo == 69:
        create_alienUFO(ai_settings, screen, ufos)
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)
    
    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_bullet()
    ship.blitme()
    bunkers.draw(screen)
    aliens.draw(screen)
    ufos.draw(screen)
    
    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, ufos, bunkers, alien_bullets):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    alien_bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.top >= 600:
            alien_bullets.remove(alien_bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets, bunkers)
    check_bullet_ufo_collision(ai_settings, screen, stats, sb, ship,
        ufos, bullets)
    check_bullet_bunker_collision(ai_settings, screen, stats, sb,
        bullets, bunkers, alien_bullets)
    check_bullet_ship_collision(ai_settings, screen, stats, sb, bullets, ship, alien_bullets, aliens)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
            
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets, bunkers):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        alien_die = pygame.mixer.Sound("songs/alien_die.wav")
        alien_die.play()
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()
        
        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
        create_bunkers(ai_settings, screen, ship, bunkers)

def check_bullet_ufo_collision(ai_settings, screen, stats, sb, ship, ufos, bullets):
    collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)

    if collisions:
        ufo_die = pygame.mixer.Sound("songs/ufo_die.wav")
        ufo_die.play()
        for ufos in collisions.values():
            points = random.randint(300, 600)
            print(points, " Points!")
            stats.score += points
            sb.prep_score()
        check_high_score(stats, sb)
        #need t rewrite to toggle space ship.....or undo...

def check_bullet_bunker_collision(ai_settings, screen, stats, sb, bullets, bunkers, alien_bullets):
    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, False)
    collisions2 = pygame.sprite.groupcollide(alien_bullets, bunkers, True, True)

    if collisions2:
        bunker_hit = pygame.mixer.Sound("songs/bunker_hit.wav")
        bunker_hit.play()
        for bunkers in collisions2.values():
            print("Bunker Hit!")

def check_bullet_ship_collision(ai_settings, screen, stats, sb, bullets, ship, alien_bullets,aliens):
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        print("Ship Hit!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

    
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def check_ufo_edges(ai_settings, ufos):
    """Respond appropriately if any aliens have reached an edge."""
    for ufo in ufos.sprites():
        if ufo.check_edges():
            change_ufo_direction(ai_settings, ufos)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def change_ufo_direction(ai_settings, ufos):
    """Drop the entire fleet, and change the fleet's direction."""
    for ufo in ufos.sprites():
        ufo.rect.y = 80
    ai_settings.ufo_direction *= -1
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets):
    ship_splode = pygame.mixer.Sound("songs/splode.wav")
    ship_splode.play()
    for index in range(36):
        clock = pygame.time.Clock()
        ship.destroy_ship(index)
        ship.blitme()
        pygame.display.flip()
        clock.tick(24)


    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        
        # Update scoreboard.
        sb.prep_ships()
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    alien_bullets.empty()
    
    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # Pause.
    sleep(0.5)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
        bullets, alien_bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
            break

def update_ufos(ai_settings, ufos):
    check_ufo_edges(ai_settings, ufos)
    ufos.update()

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, ufos, alien_bullets):
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_bullets)
            
def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows():
    """Determine the number of rows of aliens that fit on the screen."""
    number_rows = 1
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 64
    aliens.add(alien)

def create_alien2(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien2(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 128
    aliens.add(alien)

def create_alien3(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien3(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 192
    aliens.add(alien)

def create_alienUFO(ai_settings, screen, ufos):
    """Create an alien, and place it in the row."""
    ufo = AlienUFO(ai_settings, screen)
    ufo_width = ufo.rect.width
    ufo.x = 1
    ufo.rect.x = ufo.x
    ufo.rect.y = 90
    ufos.add(ufo)


def disp_bunker(ai_settings, screen, bunkers, bunker_number, row_number):
    """Create an alien, and place it in the row."""
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = bunker_width + 2 * bunker_width * bunker_number
    bunker.rect.x = bunker.x - 40
    bunker.rect.y = 475
    bunkers.add(bunker)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = 8
    number_rows = get_number_rows()
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)
            create_alien2(ai_settings, screen, aliens, alien_number,
                         row_number)
            create_alien3(ai_settings, screen, aliens, alien_number,
                          row_number)

def create_bunkers(ai_settings, screen, ship, bunkers):
    bunker = Bunker(ai_settings, screen)
    number_bunkers_x = 4
    number_rows = 1

    for row_number in range(number_rows):
        for bunker_number in range(number_bunkers_x):
            disp_bunker(ai_settings, screen, bunkers, bunker_number, row_number)
