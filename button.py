import pygame.font
class Button:
 """为游戏创建按钮的类"""
 def __init__(self, ai_game, msg):
  """初始化按钮的属性"""
  self.screen = ai_game.screen
  self.screen_rect = self.screen.get_rect()
  # Support a base color and a highlighted color.
  self.base_color = (0, 135, 0)
  self.highlighted_color = (0, 65, 0)
  self.aiplayer_color = (0, 0, 135)
  # Store the message so we can call _prep_msg() when the button color changes.
  self.msg = msg
  # 设置按钮的尺⼨和其他属性
  self.width, self.height = 200, 50
  self.button_color = self.base_color
  self.text_color = (255, 255, 255)
  self.font = pygame.font.SysFont(None, 48)
  # 创建按钮的 rect 对象，并使其居中
  self.rect = pygame.Rect(0, 0, self.width, self.height)
  self.rect.center = self.screen_rect.center
  # 按钮的标签只需创建⼀次
  self._prep_msg()
 def _prep_msg(self):
  """将 msg 渲染为图像，并使其在按钮上居中"""
  self.msg_image = self.font.render(self.msg, True, self.text_color, self.button_color)
  self.msg_image_rect = self.msg_image.get_rect()
  self.msg_image_rect.center = self.rect.center
 def _update_msg_position(self):
   """If the button has been moved, the text needs to be moved as well."""
   self.msg_image_rect.center = self.rect.center
 def set_highlighted_color(self):
  """Set the button to the highlighted color."""
  self.button_color = self.highlighted_color
  self._prep_msg()
 def set_base_color(self):
  """Set the button to the base color."""
  self.button_color = self.base_color
  self._prep_msg()
 def set_aiplayer_color(self):
  """Set the button to the base color."""
  self.button_color = self.aiplayer_color
  self._prep_msg()
 def draw_button(self):
  """绘制⼀个⽤颜⾊填充的按钮，再绘制⽂本"""
  self.screen.fill(self.button_color, self.rect)
  self.screen.blit(self.msg_image, self.msg_image_rect)