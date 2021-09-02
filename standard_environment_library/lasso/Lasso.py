from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class Lasso(Deletable, Movable, SIEffect):
	regiontype = PySI.EffectType.SI_CUSTOM
	regionname = E.id.lasso_regionname
	region_display_name = E.id.lasso_region_display_name

	def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
		super().__init__(shape, uuid, E.id.lasso_texture, Lasso.regiontype, Lasso.regionname, kwargs)
		self.qml_path = self.set_QML_path(E.id.lasso_qml_path)
		self.color = E.color.lasso_color

	@SIEffect.on_enter(E.capability.cursor_enlarge, SIEffect.RECEPTION)
	def on_enlarge_enter_recv(self):
		x, y = self.relative_x_pos(), self.relative_y_pos()
		self.shape = PySI.PointVector([[x, y], [x, y + 200], [x + 600, y + 200], [x + 600, y]])

		self.width = int(self.aabb[3].x - self.aabb[0].x)
		self.height = int(self.aabb[1].y - self.aabb[0].y)

		self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
		self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)

	@SIEffect.on_enter(E.capability.lasso_lasso, SIEffect.EMISSION)
	def on_lasso_enter_emit(self, other):
		return self._uuid

	@SIEffect.on_leave(E.capability.lasso_lasso, SIEffect.EMISSION)
	def on_lasso_leave_emit(self, other):
		return self._uuid

	@SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
	def position(self):
		x = self.x - self.last_x
		y = self.y - self.last_y
		self.last_x = self.x
		self.last_y = self.y

		return x, y, self.x, self.y