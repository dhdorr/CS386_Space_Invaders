import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image, and set its rect attribute.
        self.alien1_frames = []
        self.alien1_die = []

        alien1_sprite = SpriteSheet("images/SpriteSheet.png")
        for num_pics1 in range(24):
            image = alien1_sprite.get_image(0, 90, 32, 32)
            self.alien1_frames.append(image)
        for num_pics2 in range(24):
            image = alien1_sprite.get_image(0, 122, 32, 32)
            self.alien1_frames.append(image)

        for num_pics1 in range(4):
            image = alien1_sprite.get_image(0,282,32,32)
            self.alien1_die.append(image)
        for num_pics1 in range(4):
            image = alien1_sprite.get_image(32,282,32,32)
            self.alien1_die.append(image)
        for num_pics1 in range(4):
            image = alien1_sprite.get_image(0,314,32,32)
            self.alien1_die.append(image)
        for num_pics1 in range(4):
            image = alien1_sprite.get_image(32,314,32,32)
            self.alien1_die.append(image)

        self.image = self.alien1_frames[0]

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        self.index = 0

        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x

        self.index += 1

        if self.index >= len(self.alien1_frames):
            self.index = 0

        self.image = self.alien1_frames[self.index]



    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

