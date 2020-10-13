from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class SliderTargetDummy(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.slider_target_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(SliderTargetDummy, self).__init__(shape, uuid, "", SliderTargetDummy.regiontype, SliderTargetDummy.regionname, kwargs)
        self.color = E.id.slider_target_color

        self.enable_effect(E.id.slider_controller_capability_parent, SIEffect.RECEPTION, self.on_parent_enter_recv, None, None)

    def on_parent_enter_recv(self, parent_uuid):
        self.create_link(parent_uuid, E.id.slider_controller_capability_link_push_color, self._uuid, E.id.slider_controller_capability_link_push_color)
        self.enable_link_reception(E.id.slider_controller_capability_link_push_color, E.id.slider_controller_capability_link_push_color, self.set_color_value_from_color_value)

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
