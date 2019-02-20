class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0,0,0)
        
        # Ship settings.
        self.ship_limit = 3
            
        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 250, 250, 250
        self.alien_bullet_color = 250, 0, 0
        self.bullets_allowed = 20
        
        # Alien settings.
        self.fleet_drop_speed = 32
            
        # How quickly the game speeds up.
        self.speedup_scale = 1.25
        # How quickly the alien point values increase.
        self.score_scale = 1.5
    
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 6
        self.bullet_speed_factor = 8
        self.alien_speed_factor = 3
        
        # Scoring.
        self.alien_points = 50
    
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
        self.ufo_direction = -1
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
