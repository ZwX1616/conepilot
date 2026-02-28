import pyray as rl
from collections import deque
from openpilot.selfdrive.ui.mici.onroad import SIDE_PANEL_WIDTH
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.lib.application import gui_app
from openpilot.system.ui.widgets import Widget

MAIN_COLOR = rl.Color(*rl.LIME)
TACH_SIZE = 80
SPEED_FSZ = 28
SEG_PER_1K = 8
TACH_0K_DEG = 150
TACH_8K_DEG = 360 + 30
# TACH_TRACK_MAX = 50 # s2k fade

class Tachometer(Widget):
  def __init__(self, demo: bool = False):
    super().__init__()
    # self.track = deque([750.]*TACH_TRACK_MAX, maxlen=TACH_TRACK_MAX)
    self._background = gui_app.texture("icons_mici/onroad/driver_monitoring/dm_background.png", TACH_SIZE, TACH_SIZE)

  def _render(self, _):
    rpm = ui_state.sm['carState'].engineRpm
    gps_speed = ui_state.sm['gpsLocationExternal'].speed
    gps_mph = '%d' % (gps_speed * 2.23694)
    # self.track.append(rpm)

    main_rect = rl.Rectangle(
      self.rect.x + SIDE_PANEL_WIDTH,
      self.rect.y,
      self.rect.width - 2 * SIDE_PANEL_WIDTH,
      self.rect.height
    )

    cx = main_rect.x + main_rect.width - 60
    cy = main_rect.y + 60
    rl.draw_texture(self._background, int(cx - TACH_SIZE/2),
                    int(cy - TACH_SIZE/2),
                    rl.Color(255, 255, 255, 72))
    t_end = TACH_0K_DEG + rpm / 8000 * (TACH_8K_DEG - TACH_0K_DEG)
    rl.draw_ring(rl.Vector2(cx, cy), TACH_SIZE/2-5, TACH_SIZE/2, TACH_0K_DEG, t_end, int(SEG_PER_1K*rpm/1000), rl.Color(255, 255, 255, 128))

    tw = rl.measure_text(gps_mph, SPEED_FSZ)
    tx = cx - tw // 2
    ty = cy - SPEED_FSZ // 2
    rl.draw_text(gps_mph, int(tx), int(ty), SPEED_FSZ, MAIN_COLOR)
