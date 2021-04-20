from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.slider.SliderController import SliderController
from plugins.E import E


class SliderBase(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.slider_base_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(SliderBase, self).__init__(shape, uuid, "", SliderBase.regiontype, SliderBase.regionname, kwargs)
        self.color = E.id.slider_base_color

        self.set_QML_data("color", kwargs["color_channel"], PySI.DataType.STRING)

        self.qml_path = self.set_QML_path("SliderBase.qml")

        controller_width = E.id.slider_base_controller_width
        controller_height = E.id.slider_base_controller_height
        controller_x = self.relative_x_pos() - controller_width / 4
        controller_y = self.relative_y_pos() - controller_height / 4

        controller_shape = PySI.PointVector([[controller_x, controller_y], [controller_x, controller_y + controller_height], [controller_x + controller_width, controller_y + controller_height], [controller_x + controller_width, controller_y]])
        self.create_region_via_name(controller_shape, SliderController.regionname, False, kwargs)


    @SIEffect.on_continuous(E.id.slider_base_capability_slide, SIEffect.EMISSION)
    def on_slide_continuous_emit(self, other):
        return self.relative_x_pos(), self.width
