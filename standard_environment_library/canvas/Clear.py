from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E

class Clear(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Clear __"
    region_display_name = "Clear"

    def __init__(self, shape: PySI.PointVector=PySI.PointVector(), uuid: str="", kwargs: dict={}) -> None:
        super(Clear, self).__init__(shape, uuid, "", Clear .regiontype, Clear .regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = ""
        
    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass