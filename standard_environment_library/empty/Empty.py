from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect


class Empty(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Empty __"
    region_display_name = "Empty"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/empty.png", Empty.regiontype, Empty.regionname, kwargs)
        self.qml_path = self.set_QML_path("Empty.qml")
        # self.color = PySI.Color(128, 128, 128, 255)
