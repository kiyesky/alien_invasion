import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard:
 """显⽰得分信息的类"""
 def __init__(self, ai_game):
  """初始化显⽰得分涉及的属性"""
  self.ai_game = ai_game
  self.screen = ai_game.screen
  self.screen_rect = self.screen.get_rect()
  self.settings = ai_game.settings
  self.stats = ai_game.stats
  # 显⽰得分信息时使⽤的字体设置
  self.text_color = (30, 30, 30)
  self.font = pygame.font.SysFont(None, 48)
  self.prep_images()
 def prep_images(self):
  """准备所有的初始分数图像"""
  self.prep_score()
  self.prep_high_score()
  self.prep_level()
  self.prep_ships()
 def prep_score(self):
  """将得分渲染为图像"""
  rounded_score = round(self.stats.score, -1)
  score_str = f"{rounded_score:,}"
  self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
  # 在屏幕右上⾓显⽰得分
  self.score_rect = self.score_image.get_rect()
  self.score_rect.right = self.screen_rect.right - 20
  self.score_rect.top = 20
 def prep_high_score(self):
  """将最⾼分渲染为图像"""
  high_score = round(self.stats.high_score, -1)
  high_score_str = f"{high_score:,}"
  self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
  # 将最⾼分放在屏幕顶部的中央
  self.high_score_rect = self.high_score_image.get_rect()
  self.high_score_rect.centerx = self.screen_rect.centerx
  self.high_score_rect.top = self.score_rect.top
 def prep_level(self):
  """将等级渲染为图像"""
  level_str = str(self.stats.level)
  self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
  # 将等级放在得分下⽅
  self.level_rect = self.level_image.get_rect()
  self.level_rect.right = self.score_rect.right
  self.level_rect.top = self.score_rect.bottom + 10
 def prep_ships(self):
  """显⽰还余下多少艘⻜船"""
  self.ships = Group()
  for ship_number in range(self.stats.ships_left):
   ship = Ship(self.ai_game)
   ship.rect.x = 10 + ship_number * ship.rect.width
   ship.rect.y = 10
   self.ships.add(ship)
 def check_high_score(self):
  """检查是否诞⽣了新的最⾼分"""
  if self.stats.score > self.stats.high_score:
   self.stats.high_score = self.stats.score
   self.prep_high_score()
 def show_score(self):
  """在屏幕上绘制得分、等级和余下的⻜船数"""
  self.screen.blit(self.score_image, self.score_rect)
  self.screen.blit(self.high_score_image, self.high_score_rect)
  self.screen.blit(self.level_image, self.level_rect)
  self.ships.draw(self.screen)
