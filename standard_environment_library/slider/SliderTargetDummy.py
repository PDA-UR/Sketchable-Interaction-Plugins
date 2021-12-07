from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable


class SliderTargetDummy(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.slider_target_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", SliderTargetDummy.regiontype, SliderTargetDummy.regionname, kwargs)
        self.color = E.color.slider_target_color

    @SIEffect.on_enter("__SLIDE__", SIEffect.RECEPTION)
    def on_parent_enter_recv(self, parent_uuid):
        self.create_link(parent_uuid, E.capability.slider_controller_link_push_color, self._uuid, E.capability.slider_controller_link_push_color)

    @SIEffect.on_link(SIEffect.RECEPTION, E.capability.slider_controller_link_push_color, E.capability.slider_controller_link_push_color)
    def set_color_value_from_color_value(self, values):
        channel = values["channel"]
        color_value = values["col"]

        if channel == "r":
            self.color = PySI.Color(color_value, self.color.g, self.color.b, self.color.a)
        if channel == "g":
            self.color = PySI.Color(self.color.r, color_value, self.color.b, self.color.a)
        if channel == "b":
            self.color = PySI.Color(self.color.r, self.color.g, color_value, self.color.a)
        if channel == "a":
            self.color = PySI.Color(self.color.r, self.color.g, self.color.b, color_value)
