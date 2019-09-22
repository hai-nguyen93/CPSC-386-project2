class Settings:
    """A class to store all settings of the game"""
    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.scr_width = 900
        self.scr_height = 600
        self.bg_color = (230, 230, 230)

        # Ship's settings
        self.ship_speed_factor = 3
        self.ship_limit = 3

        # Bullet's settings
        self.bullet_speed_factor = 4
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # Alien's settings
        self.alien_speed_factor = 3
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # Speed up scale
        self.speedup_scale = 1.2
        self.drop_speed_scale = 2

        # Scoring
        self.alien_points = 50
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 3
        self.fleet_drop_speed = 10
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed += self.drop_speed_scale
        self.alien_points = int(self.alien_points * self.score_scale)
