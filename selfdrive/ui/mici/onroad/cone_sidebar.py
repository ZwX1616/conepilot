import pyray as rl
from openpilot.selfdrive.ui.mici.onroad import SIDE_PANEL_WIDTH
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.widgets import Widget

SIDEBAR_WIDTH = SIDE_PANEL_WIDTH - 4

class ConeSidebar(Widget):
  def __init__(self, demo: bool = False):
    super().__init__()
    side_img = rl.load_image("../assets/images/cone_side.png")
    self.side_tex = rl.load_texture_from_image(side_img)
    rl.unload_image(side_img)

  def _render(self, _):
    side_rect = rl.Rectangle(
      0,
      self.rect.y,
      SIDEBAR_WIDTH,
      self.rect.height,
    )

    rl.draw_texture(self.side_tex, 4, 0, rl.Color(160, 160, 160, 255))

