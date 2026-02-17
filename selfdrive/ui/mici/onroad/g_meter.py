import pyray as rl
from collections import deque
from openpilot.selfdrive.ui.mici.onroad import SIDE_PANEL_WIDTH
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.lib.application import gui_app
from openpilot.system.ui.widgets import Widget

MAIN_COLOR = rl.Color(*rl.LIME)
G_METER_SIZE = 80
G_METER_MAX = 1.5
G_TRACK_MAX = 40
G_TRACK_SMOOTH_N = 5 # 100/5 = 20Hz


class GMeter(Widget):
  def __init__(self, demo: bool = False):
    super().__init__()
    self.track = deque([(0.0,0.0)]*G_TRACK_MAX, maxlen=G_TRACK_MAX)
    self._background = gui_app.texture("icons_mici/onroad/driver_monitoring/dm_background.png", G_METER_SIZE, G_METER_SIZE)

  def _render(self, _):
    accelerometer = ui_state.sm['accelerometer']
    new_g = (accelerometer.acceleration.v[1] / 9.81,
      -accelerometer.acceleration.v[2] / 9.81)
    self.track.append(new_g)

    main_rect = rl.Rectangle(
      self.rect.x + SIDE_PANEL_WIDTH,
      self.rect.y,
      self.rect.width - 2 * SIDE_PANEL_WIDTH,
      self.rect.height
    )

    cx = main_rect.x + 60
    cy = main_rect.y + 60
    rl.draw_texture(self._background, int(cx - G_METER_SIZE/2),
                    int(cy - G_METER_SIZE/2),
                    rl.Color(255, 255, 255, 72))
    lt = list(self.track)
    for i in range(G_TRACK_MAX//G_TRACK_SMOOTH_N):
      g_chunk = lt[G_TRACK_MAX-G_TRACK_SMOOTH_N*i-G_TRACK_SMOOTH_N:G_TRACK_MAX-G_TRACK_SMOOTH_N*i]
      _gx, _gy = zip(*g_chunk)
      px = sum(_gx) / len(_gx) / G_METER_MAX * G_METER_SIZE / 2 + cx
      py = sum(_gy) / len(_gy) / G_METER_MAX * G_METER_SIZE / 2 + cy
      t = max(0, min(255, 255 - i * 30))
      col = rl.Color(MAIN_COLOR.r, MAIN_COLOR.g, MAIN_COLOR.b, t)
      rl.draw_circle(int(px), int(py), 5, col)

