from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable


class Highlight(Movable, Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__Highlight__"
    region_display_name = "Highlight"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Highlight, self).__init__(shape, uuid, "", Highlight.regiontype, Highlight.regionname, kwargs)
        self.color = PySI.Color(255, 255, 0, 128)
        self.with_border = False

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid):
        if len(self.linked_highlight_sids) > 0:
            for r in self.current_regions():
                if hasattr(r, "s_id"):
                    if r.s_id in self.linked_highlight_sids:
                        self.create_link(r._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        rel_x = self.x - self.last_x
        rel_y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return rel_x, rel_y, self.x, self.y

