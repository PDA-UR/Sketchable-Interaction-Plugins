from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from plugins.standard_environment_library.tangible.camera.ArUcoMarker import ArUcoMarker


class TableArea(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ TableArea __"
    region_display_name = "TableArea"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(TableArea, self).__init__(shape, uuid, "", TableArea.regiontype, TableArea.regionname, kwargs)
        self.source = "libStdSI"
        self.color = PySI.Color(255, 0, 0, 0)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        print(self.context_dimensions())

        size = 200
        x, y = size, size
        w, h = self.context_dimensions()
        w -= size
        h -= size

        print([[x, y], [x, y + size], [x + size, y + size], [x + size, y]])
        print([[x, h - size], [x, h], [x + size, h], [x + size, h - size]])
        print([[w - size, h - size], [w - size, h], [w, h], [w, h - size]])
        print([[w - size, y], [w - size, y + size], [w, y + size], [w, y]])

        self.create_region_via_name(PySI.PointVector([[x, y], [x, y + size], [x + size, y + size], [x + size, y]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_0.png"})
        self.create_region_via_name(PySI.PointVector([[x, h - size], [x, h], [x + size, h], [x + size, h - size]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_1.png"})
        self.create_region_via_name(PySI.PointVector([[w - size, h - size], [w - size, h], [w, h], [w, h - size]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_2.png"})
        self.create_region_via_name(PySI.PointVector([[w - size, y], [w - size, y + size], [w, y + size], [w, y]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_3.png"})



