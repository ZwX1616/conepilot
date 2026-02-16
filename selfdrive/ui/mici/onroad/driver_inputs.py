import pyray as rl
from openpilot.selfdrive.ui.mici.onroad import SIDE_PANEL_WIDTH
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.widgets import Widget
from openpilot.selfdrive.ui.mici.onroad.torque_bar import TorqueBar

BRAKE_MAX = 100
GAS_MAX = 100
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
    rl.draw_rectangle(int(side_rect.x), int(side_rect.height - brake_height),
      int(SIDE_PANEL_WIDTH / 2), brake_height, rl.RED)

    gas_height = max(1, int(ui_state.sm['carState'].gas / GAS_MAX * self.rect.height))
    rl.draw_rectangle(int(side_rect.x + SIDE_PANEL_WIDTH / 2), int(side_rect.height - gas_height),
      int(SIDE_PANEL_WIDTH / 2), gas_height, rl.GREEN)

    self._sa_bar.render(main_rect)

