from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E

class Lassoable(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__LASSOABLE__"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super(Lassoable, self).__init__(shape, uuid, r, t, s, kwargs)
        self.source = "libStdSI"

    @SIEffect.on_enter(E.capability.lasso_lasso, SIEffect.RECEPTION)
    def on_lasso_enter_recv(self, parent_uuid):
        self.create_link(parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_leave(E.capability.lasso_lasso, SIEffect.RECEPTION)
    def on_lasso_leave_recv(self, parent_uuid):
        self.remove_link(parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        self.move(self.x + rel_x, self.y + rel_y)
        self.delta_x, self.delta_y = rel_x, rel_y