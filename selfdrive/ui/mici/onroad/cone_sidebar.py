import pyray as rl
from openpilot.selfdrive.ui.mici.onroad import SIDE_PANEL_WIDTH
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.widgets import Widget

SIDEBAR_WIDTH = SIDE_PANEL_WIDTH - 4

def draw_triangle_cone48(x, y, scale=6, color=None, outline=True):
    # 48x48 triangle with flat base, centered
    s = int(scale)
    col = color or rl.Color(245, 130, 20, 255)
    out = rl.fade(rl.BLACK, 0.35)

    # vertices in "pixel space" (0..47)
    ax, ay = 24, 2
    bx, by = 6, 45
    cx, cy = 42, 45

    # draw filled triangle
    rl.draw_triangle(
        rl.Vector2(x + ax*s, y + ay*s),
        rl.Vector2(x + bx*s, y + by*s),
        rl.Vector2(x + cx*s, y + cy*s),
        col
    )

    # optional outline
    if outline:
        rl.draw_line_ex(rl.Vector2(x + ax*s, y + ay*s), rl.Vector2(x + bx*s, y + by*s), max(1, s//2), out)
        rl.draw_line_ex(rl.Vector2(x + bx*s, y + by*s), rl.Vector2(x + cx*s, y + cy*s), max(1, s//2), out)
        rl.draw_line_ex(rl.Vector2(x + cx*s, y + cy*s), rl.Vector2(x + ax*s, y + ay*s), max(1, s//2), out)


class ConeSidebar(Widget):
  def __init__(self, demo: bool = False):
    super().__init__()

  def _render(self, _):
    side_rect = rl.Rectangle(
      0,
      self.rect.y,
      SIDEBAR_WIDTH,
      self.rect.height,
    )

  draw_triangle_cone48(int(0), 0, scale=1)

