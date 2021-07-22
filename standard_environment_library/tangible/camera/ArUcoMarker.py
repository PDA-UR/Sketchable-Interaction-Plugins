from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect

class ArUcoMarker(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ArUcoMarker __"
    region_display_name = "ArUcoMarker"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ArUcoMarker, self).__init__(shape, uuid, kwargs["texture"], ArUcoMarker.regiontype, ArUcoMarker.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = self.set_QML_path("ArUcoMarker.qml")

        self.set_QML_data("img_width", self.width, PySI.DataType.INT)
        self.set_QML_data("img_height", self.height, PySI.DataType.INT)