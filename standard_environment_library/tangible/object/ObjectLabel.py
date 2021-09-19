from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class ObjectLabel(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ObjectLabel __"
    region_display_name = "ObjectLabel"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ObjectLabel, self).__init__(shape, uuid, "", ObjectLabel.regiontype, ObjectLabel.regionname, kwargs)
        self.color = PySI.Color(255, 0, 0, 0)
        self.parent_uuid = kwargs["parent_uuid"]
        self.qml_path = self.set_QML_path("Object.qml")
        self.with_border = False

        self.set_QML_data("width", self.width, PySI.DataType.INT)
        self.set_QML_data("height", self.height, PySI.DataType.INT)

        first_line = kwargs["data"][0] if len(kwargs["data"]) > 0 else ""
        second_line = kwargs["data"][1] if len(kwargs["data"]) > 1 else ""
        third_line = kwargs["data"][2] if len(kwargs["data"]) > 2 else ""
        fourth_line = kwargs["data"][3] if len(kwargs["data"]) > 3 else ""

        self.set_QML_data("first_line", first_line, PySI.DataType.STRING)
        self.set_QML_data("second_line", second_line, PySI.DataType.STRING)
        self.set_QML_data("third_line", third_line, PySI.DataType.STRING)
        self.set_QML_data("fourth_line", fourth_line, PySI.DataType.STRING)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        self.create_link(self.parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        # print(rel_x, rel_y)
        self.x += rel_x
        self.y += rel_y

