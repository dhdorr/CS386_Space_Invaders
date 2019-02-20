import pygame
from settings import Settings

class SpriteSheet(object):
    """Class used to grab images out of a sprite sheet"""

    def __init__(self, file_name="images/SpriteSheet.png"):

        ss_settings = Settings()
        """Constructor used to garb images out of a sprite sheet"""

        #Load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """Grab a single image out of a larger spritesheet
           Pass in the x, y location of the sprite
           and the width and height of the sprite."""

        #Create a new blank image
        image = pygame.Surface([width, height]).convert()

        #Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        #Assumiing black works as the transparent color change to bg_color
        bg_color = (230, 230, 230)

        image.set_colorkey(bg_color)

        #Return the image
        return image
"""
    def player_ship(self):
        #FROM Sprite sheet example arrays that store location of images
        self.player_frames = []

        #sprite_sheet = SpriteSheet("images/SpriteSheet.png")
        player_sprite = self.sprite_sheet
        #Load all the right facing images into a list
        image = player_sprite.get_image(0, 128, 32, 32)
        self.player_frames.append(image)
        image = player_sprite.get_image(32, 128, 32, 32)
        self.player_frames.append(image)
        image = player_sprite.get_image(0, 160, 32, 32)
        self.player_frames.append(image)
        image = player_sprite.get_image(32, 160, 32, 32)
        self.player_frames.append(image)

        player_image = self.player_frames[0]
        return player_image

    def alien_1(self):
        self.alien1_frames = []

        alien1_sprite = self.sprite_sheet

        image = alien1_sprite.get_image(0, 0, 32, 32)
        self.alien1_frames.append(image)
        image = alien1_sprite.get_image(0, 32, 32, 32)
        self.alien1_frames.append(image)

        alien1_image = self.alien1_frames[0]
        return alien1_image"""
