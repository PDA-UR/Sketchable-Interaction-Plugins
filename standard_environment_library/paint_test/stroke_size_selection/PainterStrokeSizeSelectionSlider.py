from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.paint_test.stroke_size_selection.PainterStrokeSizeSelectionSliderHandle import PainterStrokeSizeSelectionSliderHandle
from plugins.E import E


class PainterStrokeSizeSelectionSlider(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ PainterStrokeSizeSelectionSlider __"
    region_display_name = "PainterStrokeSizeSelectionSlider"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", PainterStrokeSizeSelectionSlider.regiontype, PainterStrokeSizeSelectionSlider.regionname, kwargs)
        self.color = PySI.Color(0, 0, 0, 255)
        controller_x = self.relative_x_pos() + self.width / 2 - E.id.slider_base_controller_width / 2
        controller_y = self.relative_y_pos() - self.height / 2

        kwargs["slider"] = self._uuid
        controller_shape = PySI.PointVector([[controller_x, controller_y], [controller_x, controller_y + E.id.slider_base_controller_height], [controller_x + E.id.slider_base_controller_width, controller_y + E.id.slider_base_controller_height], [controller_x + E.id.slider_base_controller_width, controller_y]])
        self.create_region_via_name(controller_shape, PainterStrokeSizeSelectionSliderHandle.regionname, False, kwargs)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_continuous(E.capability.slider_base_slide, SIEffect.EMISSION)
    def on_slide_continuous_emit(self, other):
        return self.x + self.relative_x_pos(), self.width

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y