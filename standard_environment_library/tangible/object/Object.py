from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E

from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library.tangible.object.ObjectLabel import ObjectLabel

import datetime

class Object(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Object __"
    region_display_name = "Object"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Object, self).__init__(shape, uuid, "", Object.regiontype, Object.regionname, kwargs)
        self.with_border = True
        self.last_x = self.aabb[3].x
        self.last_y = self.aabb[3].y
        self.border_color = PySI.Color(255, 255, 255, 255)

        self.lines = {
            -10: [str(datetime.datetime.today().strftime('%d.%m.%Y')), "3 neue Emails", "Akkustand: 65%"],
            -11: ["Länge: 17.5 cm", "Breite: 7.5 cm", "Höhe: 2.5 cm"],
            -12: ["Orange"],
            -13: ["DE: Zitrone", "EN: Lemon", "ES: Citrus", "FR: Citron"],
        }

        self.offset = 40

        self.color = PySI.Color(255, 255, 0, 0)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        x, y = self.absolute_x_pos() + self.aabb[3].x - self.aabb[0].x, self.absolute_y_pos()
        w, h = 500, 500
        shape = [[x + self.offset, y], [x + self.offset, y + h], [x + self.offset + w, y + h], [x + self.offset + w, y]]

        self.create_region_via_name(PySI.PointVector(shape), ObjectLabel.regionname, False, {"parent_uuid": self._uuid, "data": self.lines[self.s_id]})

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        self.emit_linking_action(self._uuid, PySI.LinkingCapability.POSITION, self.position())

    @SIEffect.on_leave("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_leave_recv(self, canvas_uuid: str) -> None:
        for r in self.current_regions():
            if hasattr(r, "parent_uuid"):
                if r.parent_uuid == self._uuid:
                    self.delete(r._uuid)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        rel_x = self.aabb[3].x - self.last_x
        rel_y = self.aabb[3].y - self.last_y
        self.last_x = self.aabb[3].x
        self.last_y = self.aabb[3].y

        return rel_x, rel_y, self.last_x, self.last_y
    
    def __update__(self, data):
        self.shape = data["contour"]
        
        super(Object, self).__update__(data)