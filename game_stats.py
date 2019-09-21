class GameStats:
    """Track statistics for the game"""
    def __init__(self, game_settings):
        self.settings = game_settings
        self.ships_left = self.settings.ship_limit
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
