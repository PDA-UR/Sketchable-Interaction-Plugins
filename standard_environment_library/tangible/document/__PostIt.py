from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible


class PostIt(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ PostIt __"
    region_display_name = "PostIt"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(PostIt, self).__init__(shape, uuid, "", PostIt.regiontype, PostIt.regionname, kwargs)
        self.with_border = True
        self.color = PySI.Color(0, 0, 0, 0)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass
