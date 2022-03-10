from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class PainterStrokeSizeSelectionSliderHandle(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ PainterStrokeSizeSelectionSliderHandle __"
    region_display_name = "PainterStrokeSizeSelectionSliderHandle"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", PainterStrokeSizeSelectionSliderHandle.regiontype, PainterStrokeSizeSelectionSliderHandle.regionname, kwargs)
        self.color = E.color.slider_controller_color
        self.slider_uuid = kwargs["slider"]
        self.create_link(self.slider_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.stroke_width = 4

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_continuous(E.capability.slider_base_slide, SIEffect.RECEPTION)
    def on_slide_continuous_recv(self, x: float, width: float) -> None:
        percentage = ((self.x + self.relative_x_pos() + self.width / 2 - x) / width) * 100
        percentage = 4 if percentage < 4 else percentage
        percentage = 100 if percentage > 100 else percentage

        if self.is_under_user_control:
            if self.stroke_width != percentage:
                self.stroke_width = percentage

    @SIEffect.on_continuous("__ SET_PAINTER_STROKE_WIDTH __", SIEffect.EMISSION)
    def on_set_painter_stroke_width_continuous_emit(self, other) -> float:
        return self.stroke_width, self.is_under_user_control

