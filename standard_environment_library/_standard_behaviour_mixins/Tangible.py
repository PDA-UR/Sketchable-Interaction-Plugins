from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E

class Tangible(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__Tangible__"
    region_display_name = "Tangible"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super(Tangible, self).__init__(shape, uuid, r, t, s, kwargs)

        self.s_id = kwargs["s_id"]
        self.angle = kwargs["angle"]
        self.source = "libStdSI"
        self.qml_path = ""