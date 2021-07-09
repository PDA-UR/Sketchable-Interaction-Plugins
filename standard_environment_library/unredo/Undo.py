from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
import dill
from copy import deepcopy
import pickle

class Undo(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Undo __"
    region_display_name = "Undo"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Undo, self).__init__(shape, uuid, "res/undo.png", Undo.regiontype, Undo.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = self.set_QML_path("Undo.qml")

    @SIEffect.on_enter("undo", SIEffect.EMISSION)
    def __on_undo_enter_emit__(self, other):
        pass
