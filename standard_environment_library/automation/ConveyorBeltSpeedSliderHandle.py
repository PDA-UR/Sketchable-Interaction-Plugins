from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.E import E


class ConveyorBeltSpeedSliderHandle(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ConveyorBeltSpeedSliderHandle __"
    region_display_name = "ConveyorBeltSpeedSliderHandle"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ConveyorBeltSpeedSliderHandle, self).__init__(shape, uuid, "", ConveyorBeltSpeedSliderHandle.regiontype, ConveyorBeltSpeedSliderHandle.regionname, kwargs)
        self.color = E.color.slider_controller_color
        self.qml_path = self.set_QML_path("ConveyorBeltSpeedSliderHandle.qml")
        self.speed = 250
        self.speed_value = 0

        self.set_QML_data("containerwidth", self.width, PySI.DataType.INT)
        self.set_QML_data("containerheight", self.height, PySI.DataType.INT)
        self.set_QML_data("text", str(abs(int(self.speed_value))), PySI.DataType.STRING)

        self.parent_uuid = kwargs["parent"]
        self.slider_uuid = kwargs["slider"]

        self.create_link(self.parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.create_link(self._uuid, "push_speed", self.parent_uuid, "push_speed")
        self.emit_linking_action(self._uuid, "push_speed", self.speed_output_emit())

    @SIEffect.on_continuous(E.capability.slider_base_slide, SIEffect.RECEPTION)
    def on_slide_continuous_recv(self, x: float, width: float) -> None:
        percentage = ((self.x + self.relative_x_pos() + self.width / 2 - x) / width)
        percentage = 0 if percentage < 0 else percentage
        percentage = 100 if percentage > 100 else percentage

        speed = self.speed * 2 * percentage - self.speed
        speed = -self.speed if speed < -self.speed else speed
        speed = self.speed if speed > self.speed else speed

        self.set_QML_data("text", str(abs(int(speed))), PySI.DataType.STRING)

        if not self.is_under_user_control:
            if self.speed_value != speed:
                self.speed_value = speed
                self.emit_linking_action(self._uuid, "push_speed", self.speed_output_emit())

    @SIEffect.on_enter(E.capability.slider_controller_parent, SIEffect.EMISSION)
    def on_parent_enter_emit(self, other):
        return self._uuid

    @SIEffect.on_link(SIEffect.EMISSION, "push_speed")
    def speed_output_emit(self) -> tuple:
        return self.speed_value, self.slider_uuid, self._uuid
