from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable


class SliderController(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.slider_controller_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(SliderController, self).__init__(shape, uuid, "", SliderController.regiontype, SliderController.regionname, kwargs)

        self.color = E.color.slider_controller_color
        self.color_value = E.id.slider_controller_min_value
        self.target_color_channel = kwargs[E.id.slider_controller_color_channel]

    @SIEffect.on_continuous(E.capability.slider_base_slide, SIEffect.RECEPTION)
    def on_slide_continuous_recv(self, x, width):
        color_value = abs((x - self.x) - x) / width * E.id.slider_controller_max_value

        color_value = E.id.slider_controller_min_value if color_value < E.id.slider_controller_min_value else color_value
        color_value = E.id.slider_controller_max_value if color_value > E.id.slider_controller_max_value else color_value

        if self.color_value != color_value:
            self.color_value = color_value
            self.emit_linking_action(self._uuid, E.id.slider_controller_capability_link_push_color, self.push_color_output)

    @SIEffect.on_link(SIEffect.EMISSION, E.capability.slider_controller_link_push_color)
    def push_color_output(self):
        return {"col": (self.color_value), "channel": self.target_color_channel}

    @SIEffect.on_enter(E.capability.slider_controller_parent, SIEffect.EMISSION)
    def on_parent_enter_emit(self, other):
        return self._uuid
