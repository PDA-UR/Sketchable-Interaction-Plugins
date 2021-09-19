from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from plugins.standard_environment_library.tangible.document.draw.Stroke import Stroke
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible


class TableClear(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ TableClear __"
    region_display_name = "TableClear"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(TableClear, self).__init__(shape, uuid, "", TableClear.regiontype, TableClear.regionname, kwargs)
        self.with_border = False

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        for r in self.current_regions():
            if r.regionname == Stroke.regionname:
                r.delete()
