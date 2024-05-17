import sys
from time import sleep
import json
from pathlib import Path
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
import sound_effects as se
from random import random
from ai_player import AIPlayer

class AlienInvasion:
 """管理游戏资源和⾏为的类"""
 def __init__(self):
  """初始化游戏并创建游戏资源"""
  pygame.init()
  self.clock = pygame.time.Clock()
  self.settings = Settings()
  self.ai_player = AIPlayer(self)
  # 全屏显示游戏
  self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  self.settings.screen_width = self.screen.get_rect().width
  self.settings.screen_height = self.screen.get_rect().height
  # 按settings.py中屏幕设置的分辨率创建游戏窗口显示
  # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
  # pygame.display.set_caption("Alien Invasion")
  # 创建存储游戏统计信息的实例，并创建记分牌
  self.stats = GameStats(self)
  self.sb = Scoreboard(self)
  self.ship = Ship(self)
  self.bullets = pygame.sprite.Group()
  self.aliens = pygame.sprite.Group()
  self._create_fleet()
  # 创建 Play 按钮
  self.play_button = Button(self, "Play")
  # Make difficulty level buttons.
  self._make_difficulty_buttons()
  # 创建 AIPlayer 按钮
  self._make_aiplayer_buttons()
  # 让游戏在⼀开始处于⾮活动状态
  self.game_active = False
 def _make_difficulty_buttons(self):
  """Make buttons that allow player to select difficulty level."""
  self.easy_button = Button(self, "Easy")
  self.medium_button = Button(self, "Medium")
  self.difficult_button = Button(self, "Difficult")
  # Position buttons so they don't all overlap.
  self.easy_button.rect.top = (self.play_button.rect.top + 1.5 * self.play_button.rect.height)
  self.easy_button._update_msg_position()
  self.medium_button.rect.top = (self.easy_button.rect.top + 1.5 * self.easy_button.rect.height)
  self.medium_button._update_msg_position()
  self.difficult_button.rect.top = (self.medium_button.rect.top + 1.5 * self.medium_button.rect.height)
  self.difficult_button._update_msg_position()
  # Initialize the medium button to the highlighted color.
  self.medium_button.set_highlighted_color()
 def _make_aiplayer_buttons(self):
  """定义创建 AIPlayer 按钮的方法"""
  self.aiplayer_button = Button(self, "AIPlayer")
  # 定位AIPlayer按钮，使其不会和难度等级按钮重叠
  self.aiplayer_button.rect.top = (self.play_button.rect.top - 3.5 * self.play_button.rect.height)
  self.aiplayer_button._update_msg_position()
  # 将AIPlayer按钮初始化为AIPlayer按钮定义的颜色
  self.aiplayer_button.set_aiplayer_color()
 def ai_run_game(self):
  """Replaces the original run_game(), so we can interject our own controls."""
  # 开始一个新游戏
  self._start_game()
  # Speed up the game for development work.
  self.ai_player._modify_speed(5)
  # Start the main loop for the game.
  while True:
   # Still call ai_game._check_events(), so we can use keyboard to quit.
   self._check_events()
   self._implement_strategy()
   if self.game_active:
    self.ship.update()
    self._update_bullets()
    self._update_aliens()
   else:
    break
   self._ai_update_screen()
   self.clock.tick(60)
   self._stop_ship_bullet()
 def run_game(self):
  """开始游戏的主循环"""
  while True:
   self._check_events()
   if self.game_active:
    self.ship.update()
    self._update_bullets()
    self._update_aliens()
   self._update_screen()
   self.clock.tick(60)
 def _check_events(self):
  """响应按键和⿏标事件"""
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    self._close_game()
   elif event.type == pygame.KEYDOWN:
    self._check_keydown_events(event)
   elif event.type == pygame.KEYUP:
    self._check_keyup_events(event)
   elif event.type == pygame.MOUSEBUTTONDOWN:
    mouse_pos = pygame.mouse.get_pos()
    self._check_play_button(mouse_pos)
    self._check_difficulty_buttons(mouse_pos)
    self._check_aiplayer_buttons(mouse_pos)
 def _check_play_button(self, mouse_pos):
  """在玩家单击 Play 按钮时开始新游戏"""
  button_clicked = self.play_button.rect.collidepoint(mouse_pos)
  if button_clicked and not self.game_active:
   self._start_game()
 def _check_aiplayer_buttons(self, mouse_pos):
  """在玩家单击 AIPlayer 按钮时开始AI玩家自动游戏"""
  aiplayer_button_clicked = self.aiplayer_button.rect.collidepoint(mouse_pos)
  if aiplayer_button_clicked and not self.game_active:
   self.ai_run_game()
 def _check_difficulty_buttons(self, mouse_pos):
  """Set the appropriate difficulty level."""
  easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
  medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
  diff_button_clicked = self.difficult_button.rect.collidepoint(mouse_pos)
  if easy_button_clicked:
   self.settings.difficulty_level = 'easy'
   self.easy_button.set_highlighted_color()
   self.medium_button.set_base_color()
   self.difficult_button.set_base_color()
  elif medium_button_clicked:
   self.settings.difficulty_level = 'medium'
   self.easy_button.set_base_color()
   self.medium_button.set_highlighted_color()
   self.difficult_button.set_base_color()
  elif diff_button_clicked:
   self.settings.difficulty_level = 'difficult'
   self.easy_button.set_base_color()
   self.medium_button.set_base_color()
   self.difficult_button.set_highlighted_color()
 def _start_game(self):
  """Start a new game."""
  # 还原游戏设置
  self.settings.initialize_dynamic_settings()
  # 重置游戏的统计信息
  self.stats.reset_stats()
  self.game_active = True
  self.sb.prep_images()
  # 清空外星⼈列表和⼦弹列表
  self.bullets.empty()
  self.aliens.empty()
  # 创建⼀个新的外星舰队，并将⻜船放在屏幕底部的中央
  self._create_fleet()
  self.ship.center_ship()
  # 隐藏光标
  pygame.mouse.set_visible(False)
 def _check_keydown_events(self, event):
  """响应按下"""
  if event.key == pygame.K_RIGHT:
   self.ship.moving_right = True
  elif event.key == pygame.K_LEFT:
   self.ship.moving_left = True
  elif event.key == pygame.K_SPACE:
   self._fire_bullet()
  elif event.key == pygame.K_q:
   self._close_game()
  elif (event.key == pygame.K_p) and (not self.game_active):
   # Don't start a new game during an active game, that's probably an accidental keypress.
   self._start_game()
 def _check_keyup_events(self, event):
  """响应释放"""
  if event.key == pygame.K_RIGHT:
   self.ship.moving_right = False
  elif event.key == pygame.K_LEFT:
   self.ship.moving_left = False
 def _fire_bullet(self):
  """创建⼀颗⼦弹，并将其加⼊编组 bullets """
  if len(self.bullets) < self.settings.bullets_allowed:
   new_bullet = Bullet(self)
   self.bullets.add(new_bullet)
   se.bullet_sound.play()
 def _update_bullets(self):
  """更新⼦弹的位置并删除已消失的⼦弹"""
  # 更新⼦弹的位置
  self.bullets.update()
  # 删除已消失的⼦弹
  for bullet in self.bullets.copy():
   if bullet.rect.bottom <= 0:
    self.bullets.remove(bullet)
  self._check_bullet_alien_collisions()
 def _check_bullet_alien_collisions(self):
  """响应⼦弹和外星⼈的碰撞"""
  # 删除发⽣碰撞的⼦弹和外星⼈
  collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
  if collisions:
   for aliens in collisions.values():
    self.stats.score += self.settings.alien_points * len(aliens)
   self.sb.prep_score()
   self.sb.check_high_score()
   se.alien_sound.play()
  if not self.aliens:
   self._start_new_level()
 def _start_new_level(self):
  """Start a new level, after the fleet has been cleared."""
  # 删除现有的所有⼦弹，并创建⼀个新的外星舰队
  self.bullets.empty()
  self._create_fleet()
  self.settings.increase_speed()
  # 提⾼等级
  self.stats.level += 1
  self.sb.prep_level()
 def _update_aliens(self):
  """检查是否有外星⼈位于屏幕边缘，并更新整个外星舰队的位置"""
  self._check_fleet_edges()
  self.aliens.update()
  # 检测外星⼈和⻜船之间的碰撞
  if pygame.sprite.spritecollideany(self.ship, self.aliens):
   self._ship_hit()
  # 检查是否有外星⼈到达了屏幕的下边缘
  self._check_aliens_bottom()
 def _create_fleet(self):
  """创建⼀个外星舰队"""
  # 创建⼀个外星⼈，再不断添加，直到没有空间添加外星⼈为⽌
  # 外星⼈的间距为外星⼈的宽度和外星⼈的⾼度
  alien = Alien(self)
  alien_width, alien_height = alien.rect.size
  current_x, current_y = alien_width, alien_height
  while current_y < (self.settings.screen_height - 3 * alien_height):
   while current_x < (self.settings.screen_width - 2 * alien_width):
    self._create_alien(current_x, current_y)
    current_x += 2 * alien_width
   # 添加⼀⾏外星⼈后，重置 x 值并递增 y 值
   current_x = alien_width
   current_y += 2 * alien_height
 def _create_alien(self, x_position, y_position):
  """创建⼀个外星⼈，并将其加⼊外星舰队"""
  new_alien = Alien(self)
  new_alien.x = x_position
  new_alien.rect.x = x_position
  new_alien.rect.y = y_position
  self.aliens.add(new_alien)
 def _check_fleet_edges(self):
  """在有外星⼈到达边缘时采取相应的措施"""
  for alien in self.aliens.sprites():
   if alien.check_edges():
    self._change_fleet_direction()
    break
 def _change_fleet_direction(self):
  """将整个外星舰队向下移动，并改变它们的⽅向"""
  for alien in self.aliens.sprites():
   alien.rect.y += self.settings.fleet_drop_speed
  self.settings.fleet_direction *= -1
 def _ship_hit(self):
  """响应⻜船和外星⼈的碰撞"""
  if self.stats.ships_left > 0:
   # 将 ships_left 减 1 并更新记分牌
   self.stats.ships_left -= 1
   self.sb.prep_ships()
   # 清空外星⼈列表和⼦弹列表
   self.bullets.empty()
   self.aliens.empty()
   # 创建⼀个新的外星舰队，并将⻜船放在屏幕底部的中央
   self._create_fleet()
   self.ship.center_ship()
   # 暂停
   sleep(0.5)
  else:
   self.game_active = False
   pygame.mouse.set_visible(True)
 def _check_aliens_bottom(self):
  """检查是否有外星⼈到达了屏幕的下边缘"""
  for alien in self.aliens.sprites():
   if alien.rect.bottom >= self.settings.screen_height:
    # 像⻜船被撞到⼀样进⾏处理
    self._ship_hit()
    break
 def _implement_strategy(self):
  """Implement an automated strategy for playing the game."""
  # Get specific alien to chase.
  target_alien = self._get_target_alien()
  # Move toward target alien.
  if self.ship.rect.x < target_alien.rect.x:
   self.ship.moving_right = True
   self.ship.moving_left = False
  elif self.ship.rect.x > target_alien.rect.x:
   self.ship.moving_right = False
   self.ship.moving_left = True
  # Fire a bullet at the given frequency, whenever possible.
  firing_frequency = 1.0
  if random() < firing_frequency:
   # 调用_fire_bullet方法，自动发射子弹
   self._fire_bullet()
 def _get_target_alien(self):
  """Get a specific alien to target."""
  # Find the right-most alien in the bottom row.
  # Pick the first alien in the group. Then compare all others, and return the alien with the greatest x and y rect attributes.
  target_alien = self.aliens.sprites()[0]
  for alien in self.aliens.sprites():
   if alien.rect.y > target_alien.rect.y:
    # This alien is farther down than target_alien.
    target_alien = alien
   elif alien.rect.y < target_alien.rect.y:
    # This alien is above target_alien.
    continue
   elif alien.rect.x > target_alien.rect.x:
    # This alien is in the same row, but farther right.
    target_alien = alien
  return target_alien
 def _stop_ship_bullet(self):
  for alien in self.aliens.sprites():
   if self.stats.ships_left == 0 and alien.rect.bottom >= self.settings.screen_height or pygame.sprite.spritecollideany(self.ship, self.aliens):
    self.ship.moving_right = False
    self.ship.moving_left = False
    self.bullets.empty()
    se.bullet_sound.stop()
    self.game_active = False
    pygame.mouse.set_visible(True)
    break
 def _ai_update_screen(self):
  """更新屏幕上的图像，并切换到新屏幕"""
  self.screen.fill(self.settings.bg_color)
  for bullet in self.bullets.sprites():
   bullet.draw_bullet()
  self.ship.blitme()
  self.aliens.draw(self.screen)
  # 显⽰得分
  self.sb.show_score()
  pygame.display.flip()
 def _update_screen(self):
  """更新屏幕上的图像，并切换到新屏幕"""
  self.screen.fill(self.settings.bg_color)
  for bullet in self.bullets.sprites():
   bullet.draw_bullet()
  self.ship.blitme()
  self.aliens.draw(self.screen)
  # 显⽰得分
  self.sb.show_score()
  # 如果游戏处于⾮活动状态，就绘制 Play,AIPlayer,难度等级 按钮
  if not self.game_active:
   self.play_button.draw_button()
   self.easy_button.draw_button()
   self.medium_button.draw_button()
   self.difficult_button.draw_button()
   self.aiplayer_button.draw_button()
  pygame.display.flip()
 def _close_game(self):
  """Save high score and exit."""
  saved_high_score = self.stats.get_saved_high_score()
  if self.stats.high_score > saved_high_score:
   path = Path('high_score.json')
   contents = json.dumps(self.stats.high_score)
   path.write_text(contents)
  sys.exit()

if __name__ == '__main__':
 # 创建游戏实例并运⾏游戏
 ai = AlienInvasion()
 ai.run_game()
