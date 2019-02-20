import pygame
from pygame.sprite import Sprite
from spritesheet import SpriteSheet


class Bunker(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(Bunker, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image, and set its rect attribute.
        self.bunker_frames = []

        bunker_sprite = SpriteSheet("images/SpriteSheet.png")

        image = bunker_sprite.get_image(0, 346, 96, 64)
        self.bunker_frames.append(image)
        image = bunker_sprite.get_image(0, 346, 96, 64)
        self.bunker_frames.append(image)

        self.image = self.bunker_frames[0]

        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x = 128
        self.rect.x = self.x
        self.y = 400
        self.rect.y = self.y

    def blitme(self):
        """Draw the alien at its current location."""

        self.screen.blit(self.image, self.rect)
