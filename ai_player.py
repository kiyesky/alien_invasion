
class AIPlayer:
 def __init__(self, ai_game):
  """Automatic player for Alien Invasion."""
  # Need a reference to the game object.
  self.ai_game = ai_game

 def _modify_speed(self, speed_factor):
  self.ai_game.settings.ship_speed *= speed_factor
  self.ai_game.settings.bullet_speed *= speed_factor
  self.ai_game.settings.alien_speed *= speed_factor
