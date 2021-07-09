from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

class Redo(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Redo __"
    region_display_name = "Redo"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Redo, self).__init__(shape, uuid, "res/redo.png", Redo.regiontype, Redo.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = self.set_QML_path("Redo.qml")

    @SIEffect.on_enter("redo", SIEffect.EMISSION)
    def __on_redo_enter_emit__(self, other):
        pass