from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.E import E


class TangibleDemo(Tangible, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__TangibleDemo__"
    region_display_name = "TangibleDemo"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        Tangible.__init__(self, shape, uuid, SIEffect.TEXTURE_PATH_NONE, TangibleDemo.regiontype, TangibleDemo.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, SIEffect.TEXTURE_PATH_NONE, TangibleDemo.regiontype, TangibleDemo.regionname, kwargs)

        self.color = E.id.tangible_demo_color
