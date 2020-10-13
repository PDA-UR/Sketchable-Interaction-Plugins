from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class SliderController(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.slider_controller_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(SliderController, self).__init__(shape, uuid, "", SliderController.regiontype, SliderController.regionname, kwargs)
        self.color = E.id.slider_controller_color
        self.color_value = E.id.slider_controller_min_value

        self.enable_effect(E.id.slider_base_capability_slide, SIEffect.RECEPTION, None, self.on_slide_continuous_recv, None)
        self.enable_effect(E.id.slider_controller_capability_parent, SIEffect.EMISSION, self.on_parent_enter_emit, None, None)

        self.target_color_channel = kwargs[E.id.slider_controller_color_channel]

        self.enable_link_emission(E.id.slider_controller_capability_link_push_color, self.push_color_output)

    def on_slide_continuous_recv(self, x, width):
        color_value = abs((x - self.x) - x) / width * E.id.slider_controller_max_value

        color_value = E.id.slider_controller_min_value if color_value < E.id.slider_controller_min_value else color_value
        color_value = E.id.slider_controller_max_value if color_value > E.id.slider_controller_max_value else color_value

        if self.color_value != color_value:
            self.color_value = color_value
            self.emit_linking_action(self._uuid, E.id.slider_controller_capability_link_push_color, self.push_color_output)

    def push_color_output(self):
        return {"col": (self.color_value), "channel": self.target_color_channel}

    def on_parent_enter_emit(self, other):
        return self._uuid