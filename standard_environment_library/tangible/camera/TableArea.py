from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E
from plugins.standard_environment_library.tangible.camera.ArUcoMarker import ArUcoMarker


class TableArea(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.table_area_regionname
    region_display_name = E.id.table_area_region_display_name

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(TableArea, self).__init__(shape, uuid, "", TableArea.regiontype, TableArea.regionname, kwargs)
        self.color = E.color.table_area_color

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        size = 200
        x, y = size, size
        w, h = self.context_dimensions()
        w -= size
        h -= size

        self.create_region_via_name(PySI.PointVector([[x, y], [x, y + size], [x + size, y + size], [x + size, y]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_0.png"})
        self.create_region_via_name(PySI.PointVector([[x, h - size], [x, h], [x + size, h], [x + size, h - size]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_1.png"})
        self.create_region_via_name(PySI.PointVector([[w - size, h - size], [w - size, h], [w, h], [w, h - size]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_2.png"})
        self.create_region_via_name(PySI.PointVector([[w - size, y], [w - size, y + size], [w, y + size], [w, y]]), ArUcoMarker.regionname, False, {"texture": "res/4by4_3.png"})



