import sys
import pygame
from pygame.sprite import Sprite

#maybe spritesheet implementation
from spritesheet import SpriteSheet


class Ship(pygame.sprite.Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #FROM Sprite sheet example arrays that store location of images
        self.flying_frames = []
        self.explode_frames = []

        sprite_sheet = SpriteSheet("images/SpriteSheet.png")
        #Load all the flying images into a list
        for num_pics1 in range(6):
            image = sprite_sheet.get_image(0, 218, 32, 32)
            self.flying_frames.append(image)
        for num_pics2 in range(6):
            image = sprite_sheet.get_image(32, 218, 32, 32)
            self.flying_frames.append(image)
        for num_pics3 in range(6):
            image = sprite_sheet.get_image(0, 250, 32, 32)
            self.flying_frames.append(image)
        for num_pics4 in range(6):
            image = sprite_sheet.get_image(32, 250, 32, 32)
            self.flying_frames.append(image)

        #Load all the exploding frames into a list
        for num_pics1 in range(4):
            image = sprite_sheet.get_image(0, 442, 32, 32)
            self.explode_frames.append(image)
        for num_pics2 in range(4):
            image = sprite_sheet.get_image(32, 442, 32, 32)
            self.explode_frames.append(image)
        for num_pics3 in range(4):
            image = sprite_sheet.get_image(64, 442, 32, 32)
            self.explode_frames.append(image)
        for num_pics4 in range(4):
            image = sprite_sheet.get_image(0, 474, 32, 32)
            self.explode_frames.append(image)
        for num_pics5 in range(4):
            image = sprite_sheet.get_image(32, 474, 32, 32)
            self.explode_frames.append(image)
        for num_pics6 in range(4):
            image = sprite_sheet.get_image(64, 474, 32, 32)
            self.explode_frames.append(image)
        for num_pics7 in range(4):
            image = sprite_sheet.get_image(0, 506, 32, 32)
            self.explode_frames.append(image)
        for num_pics8 in range(4):
            image = sprite_sheet.get_image(32, 506, 32, 32)
            self.explode_frames.append(image)
        for num_pics9 in range(4):
            image = sprite_sheet.get_image(64, 506, 32, 32)
            self.explode_frames.append(image)

        self.image = self.flying_frames[0]

        # Load the ship image, and get its rect. *EDITED SELF.IMAGE*

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_right = False
        self.moving_left = False

        self.index = 0
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

        self.index += 1

        if self.index >= len(self.flying_frames):
            self.index = 0

        self.image = self.flying_frames[self.index]

    def destroy_ship(self, index):
        #hopefully plays destroy animation

        self.image = self.explode_frames[index]


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
