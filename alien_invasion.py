import sys
import pygame
from pygame.sprite import Group
from pygame.locals import *

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship

import game_functions as gf
import random
pygame.init()

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")


    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Set the background color.
    bg_color = (230, 230, 230)
    
    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    bunkers = Group()
    ufos = Group()
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    black = (0,0,0)
    end_it = False
    home_page = pygame.image.load('images/homepge.png')
    while (end_it == False):
        #screen.fill(black)
        screen.blit(home_page, (100,200))
        myfont = pygame.font.SysFont("Britannic Bold", 80)
        myfont2 = pygame.font.SysFont("Britannic Bold", 40)

        nlabel = myfont.render("Space", 1, (0, 255, 0))
        big_score_label = myfont.render("=  ???", 1, (0,255,0))

        nlabe2 = myfont2.render("Invaders", 1, (255,255,255))
        score_label1 = myfont2.render("=  50", 1, (255,255,255))
        score_label2 = myfont2.render("=  50", 1, (255,255,255))
        score_label3 = myfont2.render("=  50", 1, (255,255,255))

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                end_it = True
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(nlabel, (300,100))
        screen.blit(nlabe2, (320,160))
        screen.blit(big_score_label, (300, 225))
        screen.blit(score_label1, (250, 300))
        screen.blit(score_label2, (250, 350))
        screen.blit(score_label3, (250, 400))



        pygame.display.flip()

    clock = pygame.time.Clock()
    ufo_exists = False

    # Start the main loop for the game.

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets, bunkers, ufos, alien_bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets, ufos, bunkers, alien_bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                bullets, ufos, alien_bullets)
            #if ufo_exists == True:
            gf.update_ufos(ai_settings, ufos)

        ran_num = random.randint(1,1001)
        if ufo_exists == False:
            if ran_num > 101 and ran_num < 104:
                gf.create_alienUFO(ai_settings, screen, ufos)
                ufo_exists = True
                print("Aww Lawd He Comin!")

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
            bullets, play_button, bunkers, ufos, alien_bullets)


        clock.tick(24)


run_game()
