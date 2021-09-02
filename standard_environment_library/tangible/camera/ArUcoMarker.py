from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect

from plugins.E import E


class ArUcoMarker(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.aruco_regionname
    region_display_name = E.id.aruco_region_display_name

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ArUcoMarker, self).__init__(shape, uuid, kwargs["texture"], ArUcoMarker.regiontype, ArUcoMarker.regionname, kwargs)
        self.qml_path = self.set_QML_path(E.id.aruco_qml_path)

        self.set_QML_data("img_width", self.width, PySI.DataType.INT)
        self.set_QML_data("img_height", self.height, PySI.DataType.INT)