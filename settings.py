class Settings:
 """存储游戏《外星⼈⼊侵》中所有设置的类"""
 def __init__(self):
  """初始化游戏的静态设置"""
  # 屏幕设置
  self.screen_width = 1200
  self.screen_height = 800
  self.bg_color = (230, 230, 230)
  # ⻜船设置
  self.ship_limit = 3
  # ⼦弹设置
  self.bullet_width = 3
  self.bullet_height = 15
  self.bullet_color = 60, 60, 60
  # 外星⼈设置
  self.fleet_drop_speed = 10
  # 以什么速度加快游戏的节奏
  self.speedup_scale = 1.1
  self.difficulty_level = 'medium'
  # 外星⼈分数的提⾼速度
  self.score_scale = 1.5
  self.initialize_dynamic_settings()
 def initialize_dynamic_settings(self):
  """初始化随游戏进⾏⽽变化的设置"""
  if self.difficulty_level == 'easy':
   self.ship_limit = 5
   self.bullets_allowed = 10
   self.ship_speed = 1.5
   self.bullet_speed = 3.0
   self.alien_speed = 1.0
  elif self.difficulty_level == 'medium':
   self.ship_limit = 3
   self.bullets_allowed = 3
   self.ship_speed = 3.0
   self.bullet_speed = 6.0
   self.alien_speed = 2.0
  elif self.difficulty_level == 'difficult':
   self.ship_limit = 2
   self.bullets_allowed = 3
   self.ship_speed = 6.0
   self.bullet_speed = 12.0
   self.alien_speed = 4.0
  # 记分设置
  self.alien_points = 50

  # fleet_direction 为 1 表⽰向右移动，为-1 表⽰向左移动
  self.fleet_direction = 1

 def increase_speed(self):
  """提⾼速度设置的值和外星⼈分数"""
  self.ship_speed *= self.speedup_scale
  self.bullet_speed *= self.speedup_scale
  self.alien_speed *= self.speedup_scale
  self.alien_points = int(self.alien_points * self.score_scale)

 def set_difficulty(self, diff_setting):
  if diff_setting == 'easy':
   print('easy')
  elif diff_setting == 'medium':
   pass
  elif diff_setting == 'difficult':
   pass
