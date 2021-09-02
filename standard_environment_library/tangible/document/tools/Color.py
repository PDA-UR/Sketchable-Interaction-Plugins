from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class Color(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Color __"
    region_display_name = "Color"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Color, self).__init__(shape, uuid, "", Color.regiontype, Color.regionname, kwargs)

        self.color = kwargs["color"]
        self.assigned_cursor = None

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_continuous("ASSIGN", SIEffect.EMISSION)
    def on_document_color_tool_assign_continuous_emit(self, other):
        self.assigned_cursor = other._uuid

        return self.color