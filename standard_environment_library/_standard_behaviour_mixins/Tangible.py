from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class Tangible(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__Tangible__"
    region_display_name = "Tangible"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super(Tangible, self).__init__(shape, uuid, r, t, s, kwargs)

        self.s_id = kwargs["s_id"]
        self.angle = kwargs["angle"]
        self.linked_highlight_sids = [] if "links" not in kwargs else kwargs["links"]
        self.source = "libStdSI"
