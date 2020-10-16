from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class PositionLinkable(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__POSITION_LINKABLE__"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super(PositionLinkable, self).__init__(shape, uuid, r, t, s, kwargs)

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        self.move(self.x + rel_x, self.y + rel_y)

        self.delta_x, self.delta_y = rel_x, rel_y

        if self.is_under_user_control:
            self.mouse_x = abs_x
            self.mouse_y = abs_y
        else:
            self.mouse_x = 0
            self.mouse_y = 0