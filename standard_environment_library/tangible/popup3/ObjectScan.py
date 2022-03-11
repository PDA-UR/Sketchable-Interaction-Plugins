from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class ObjectScan(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ ObjectScan __"
    region_display_name = "ObjectScan"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/scan.png", ObjectScan.regiontype, ObjectScan.regionname, kwargs)
        self.qml_path = self.set_QML_path("TangibleScan.qml")
        self.color = PySI.Color(80, 80, 0, 255)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        x, y, w, h = self.absolute_x_pos(), self.absolute_y_pos(), self.aabb[3].x - self.aabb[0].x, self.aabb[1].y - self.aabb[0].y
        self.__notify__(f"{x},{y},{w},{h}", PySI.DataType.STRING)
