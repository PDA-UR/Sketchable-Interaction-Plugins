from libPySI import PySI


from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable

class Stroke(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Stroke __"
    region_display_name = "Stroke"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", Stroke.regiontype, Stroke.regionname, kwargs)

        # self.with_border = False
        self.__tool_source__ = kwargs["tool"]
        self.__is_in_drawing__ = kwargs["is_in_drawing"]

        r, g, b = kwargs["color"].r, kwargs["color"].g, kwargs["color"].b

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass