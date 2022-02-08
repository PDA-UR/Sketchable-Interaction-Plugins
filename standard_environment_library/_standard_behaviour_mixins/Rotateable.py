from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class Rotateable(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ROTATEABLE__"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super().__init__(shape, uuid, r, t, s, kwargs)
        self.relx = 0

    @SIEffect.on_enter("__TEST_ROTATE__", SIEffect.RECEPTION)
    def on_test_rotate_enter_recv(self, other_uuid):
        self.create_link(other_uuid, PySI.LinkingCapability.POSITION, self._uuid, "__ROTATE__")

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, "__ROTATE__")
    def set_rotation_from_position(self, relx):
        if relx != self.relx:
            self.angle_degrees = 0

            if relx < 0:
                self.angle_degrees = -1
            elif relx > 0:
                self.angle_degrees = 1

            self.relx = relx