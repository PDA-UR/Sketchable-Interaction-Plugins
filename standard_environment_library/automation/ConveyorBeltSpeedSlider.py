from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable
from plugins.standard_environment_library.automation.ConveyorBeltSpeedSliderHandle import ConveyorBeltSpeedSliderHandle
from plugins.E import E


class ConveyorBeltSpeedSlider(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ConveyorBeltSpeedSlider __"
    region_display_name = "ConveyorBeltSpeedSlider"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", ConveyorBeltSpeedSlider.regiontype, ConveyorBeltSpeedSlider.regionname, kwargs)
        self.color = E.color.slider_base_color
        controller_x = self.relative_x_pos() + self.width / 2 - E.id.slider_base_controller_width / 2
        controller_y = self.relative_y_pos() - self.height / 2

        self.create_link(kwargs["parent"], PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        kwargs["slider"] = self._uuid

        controller_shape = PySI.PointVector([[controller_x, controller_y], [controller_x, controller_y + E.id.slider_base_controller_height], [controller_x + E.id.slider_base_controller_width, controller_y + E.id.slider_base_controller_height], [controller_x + E.id.slider_base_controller_width, controller_y]])
        self.create_region_via_name(controller_shape, ConveyorBeltSpeedSliderHandle.regionname, False, kwargs)

    @SIEffect.on_continuous(E.capability.slider_base_slide, SIEffect.EMISSION)
    def on_slide_continuous_emit(self, other):
        return self.x + self.relative_x_pos(), self.width