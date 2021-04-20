from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable


class Lasso(Deletable, Movable, SIEffect):
	regiontype = PySI.EffectType.SI_CUSTOM
	regionname = "__LASSO__"
	region_display_name = "Lasso"

	def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
		super(Lasso, self).__init__(shape, uuid, E.id.lasso_texture, Lasso.regiontype, Lasso.regionname, kwargs)

		self.set_QML_path("Lasso.qml")
		self.color = E.id.lasso_color

	@SIEffect.on_enter(E.id.lasso_capabiliy, SIEffect.EMISSION)
	def on_lasso_enter_emit(self, other):
		return self._uuid

	@SIEffect.on_leave(E.id.lasso_capabiliy, SIEffect.EMISSION)
	def on_lasso_leave_emit(self, other):
		return self._uuid

	@SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
	def position(self):
		x = self.x - self.last_x
		y = self.y - self.last_y
		self.last_x = self.x
		self.last_y = self.y

		return x, y, self.x, self.y
