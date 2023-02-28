from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class FPS_Counter(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ FPS_Counter __"
    region_display_name = "FPS_Counter"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FPS_Counter, self).__init__(shape, uuid, "", FPS_Counter.regiontype, FPS_Counter.regionname, kwargs)
        self.qml_path = self.set_QML_path("FPS_Counter.qml")
        self.color = PySI.Color(255, 255, 255, 255)
        self.fps = 60

        self.set_QML_data("text", f"{self.fps} FPS", PySI.DataType.STRING)

    def __update_fps__(self, actual, target):
        self.fps = actual

        if self.fps > 40:
            self.color = PySI.Color(0, 255, 0, 255)
        elif self.fps > 20:
            self.color = PySI.Color(255, 255, 0, 255)
        else:
            self.color = PySI.Color(255, 0, 0, 255)

        self.set_QML_data("text", f"{self.fps} / {target} FPS", PySI.DataType.STRING)
