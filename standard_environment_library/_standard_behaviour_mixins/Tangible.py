from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable


class Tangible(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__Tangible__"
    region_display_name = "Tangible"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super().__init__(shape, uuid, r, t, s, kwargs)
        self.object_id = kwargs["id"]
        self.links = [] if "links" not in kwargs else kwargs["links"]

    def __update__(self, data):
        pass
