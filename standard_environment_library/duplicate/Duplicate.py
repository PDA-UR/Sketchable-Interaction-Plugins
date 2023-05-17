from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class Duplicate(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Duplicate __"
    region_display_name = "Duplicate"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "res/duplicate.png", Duplicate.regiontype, Duplicate.regionname, kwargs)
        self.qml_path = self.set_QML_path("Duplicate.qml")
        self.color = PySI.Color(255, 0, 0, 255)
        pass

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_enter("__ DUPLICATE __", SIEffect.EMISSION)
    def on_duplicate_enter_emit(self, other):
        pass

    @SIEffect.on_leave("__ DUPLICATE __", SIEffect.EMISSION)
    def on_duplicate_leave_emit(self, other):
        other.is_duplicate = False
