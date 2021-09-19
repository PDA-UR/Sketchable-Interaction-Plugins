from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable


class Tangible(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__Tangible__"
    region_display_name = "Tangible"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super(Tangible, self).__init__(shape, uuid, r, t, s, kwargs)
        self.s_id = kwargs["s_id"]
        self.c_id = 0 if "c_id" not in kwargs else kwargs["c_id"]
        self.angle = kwargs["angle"]
        self.linked_highlight_sids = [] if "links" not in kwargs else kwargs["links"]
        self.finger = 0 if "finger" not in kwargs else kwargs["finger"]
        self.press = -2 if "press" not in kwargs else kwargs["press"]

    def __update__(self, data):
        self.finger = data["finger"] if "finger" in data else ""
        self.press = data["press"] if "press" in data else ""
