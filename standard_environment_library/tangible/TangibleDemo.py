from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.E import E


class TangibleDemo(Tangible, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.tangible_demo_regionname
    region_display_name = E.id.tangible_demo_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(TangibleDemo, self).__init__(shape, uuid, SIEffect.TEXTURE_PATH_NONE, TangibleDemo.regiontype, TangibleDemo.regionname, kwargs)
        self.color = E.color.tangible_demo_color

    def __update__(self, data):
        super().__update__(data)
        self.shape = data["contour"]
