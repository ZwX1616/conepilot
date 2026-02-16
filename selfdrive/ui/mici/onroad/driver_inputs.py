import pyray as rl
from openpilot.selfdrive.ui.mici.onroad import SIDE_PANEL_WIDTH
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.widgets import Widget
from openpilot.selfdrive.ui.mici.onroad.torque_bar import TorqueBar

BRAKE_MAX = 100
GAS_MAX = 100
PEDAL_FADE_MIN = 70
PEDAL_FADE_MAX = 255

STEER_MAG_MAX = 270

class fake_fof():
  def __init__(self, x0=0., rc=0.1, dt=0.1):
    self.x = x0

  def update(self, x):
    pass

class SteerAngleBar(TorqueBar):
  def __init__(self):
    super().__init__()
    self._torque_filter = fake_fof()
    self._torque_line_alpha_filter = fake_fof(1.0)

  def _render(self, rect):
    self._torque_filter.x = ui_state.sm['carState'].steeringAngleDeg / STEER_MAG_MAX
    super()._render(rect)


def as_color(c):
  if isinstance(c, (tuple, list)):
    if len(c) == 3: return rl.Color(c[0], c[1], c[2], 255)
    return rl.Color(c[0], c[1], c[2], c[3])
  return c

def with_alpha(c, a) -> rl.Color:
  c = as_color(c)
  return rl.Color(c.r, c.g, c.b, min(255,max(0,int(a))))

def draw_capsule_vfade(rect: rl.Rectangle, top_color, bottom_color):
  top_color = as_color(top_color)
  bottom_color = as_color(bottom_color)

  x, y, w, h = rect.x, rect.y, rect.width, rect.height
  w_i, h_i = max(1, int(w)), max(1, int(h))
  x_i, y_i = int(x), int(y)

  r = w_i // 2
  if h_i <= 2*r:
    # Too short: just a circle-ish blob
    rl.draw_circle(x_i + r, y_i + h_i//2, max(1, h_i//2), top_color)
    return

  # Body (exclude caps so nothing overlaps)
  body_x = x_i
  body_y = y_i + r
  body_w = w_i
  body_h = h_i - 2*r

  # Gradient body (solid at top -> transparent at bottom, or whatever you pass)
  rl.draw_rectangle_gradient_v(body_x, body_y, body_w, body_h, top_color, bottom_color)

  cx = x_i + r

  # Top cap: draw a circle but clip to top half only
  rl.begin_scissor_mode(body_x, y_i, body_w, r)
  rl.draw_circle(cx, y_i + r, r, top_color)
  rl.end_scissor_mode()

  # Bottom cap: draw a circle but clip to bottom half only
  rl.begin_scissor_mode(body_x, y_i + h_i - r, body_w, r)
  rl.draw_circle(cx, y_i + h_i - r, r, bottom_color)
  rl.end_scissor_mode()


class DriverInputs(Widget):
  def __init__(self, demo: bool = False):
    super().__init__()
    self._sa_bar = SteerAngleBar()

  def _render(self, _):
    main_rect = rl.Rectangle(
      self.rect.x + SIDE_PANEL_WIDTH,
      self.rect.y,
      self.rect.width - 2 * SIDE_PANEL_WIDTH,
      self.rect.height
    )
    side_rect = rl.Rectangle(
      self.rect.x + self.rect.width - SIDE_PANEL_WIDTH,
      self.rect.y,
      SIDE_PANEL_WIDTH,
      self.rect.height,
    )

    brake_height = max(1, int(ui_state.sm['carState'].brake / BRAKE_MAX * self.rect.height))
    draw_capsule_vfade(rl.Rectangle(side_rect.x,
        side_rect.y + side_rect.height - brake_height,
        SIDE_PANEL_WIDTH/2,
        brake_height),
      with_alpha(rl.RED, PEDAL_FADE_MIN + brake_height / self.rect.height * (PEDAL_FADE_MAX-PEDAL_FADE_MIN)),
      with_alpha(rl.RED, PEDAL_FADE_MIN))

    gas_height = max(1, int(ui_state.sm['carState'].gas / GAS_MAX * self.rect.height))
    draw_capsule_vfade(rl.Rectangle(side_rect.x + SIDE_PANEL_WIDTH / 2,
        side_rect.y + side_rect.height - gas_height,
        SIDE_PANEL_WIDTH/2,
        gas_height),
      with_alpha(rl.GREEN, PEDAL_FADE_MIN + gas_height / self.rect.height * (PEDAL_FADE_MAX-PEDAL_FADE_MIN)),
      with_alpha(rl.GREEN, PEDAL_FADE_MIN))

    self._sa_bar.render(main_rect)

