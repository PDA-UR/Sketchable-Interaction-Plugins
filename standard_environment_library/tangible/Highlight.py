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
        self.visible = False

        self.x_in_document = kwargs["orig_x"]
        self.y_in_document = kwargs["orig_y"]
        self.width_in_document = kwargs["orig_width"]
        self.height_in_document = kwargs["orig_height"]

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid):
            for r in self.current_regions():
                if hasattr(r, "s_id"):
                    if len(self.linked_highlight_sids) > 0:
                        if r.s_id in self.linked_highlight_sids:
                            self.create_link(r._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

                    if r.s_id == self.c_id:
                        self.create_link(r._uuid, "ADD_HIGHLIGHT", self._uuid, "ADD_HIGHLIGHT")
                        self.emit_linking_action(r._uuid, "ADD_HIGHLIGHT", r.on_add_highlight_link_emit())

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        rel_x = self.x - self.last_x
        rel_y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return rel_x, rel_y, self.x, self.y

    @SIEffect.on_link(SIEffect.RECEPTION, "ADD_HIGHLIGHT", "ADD_HIGHLIGHT")
    def on_add_highlight_link_recv(self, doc_x, doc_y, width_fraction, height_fraction, doc_x_axis, doc_y_axis) -> None:
        x = self.x_in_document * width_fraction
        y = self.y_in_document * height_fraction
        width = self.width_in_document * width_fraction
        height = self.height_in_document * height_fraction

        highlight_tlc_x = doc_x + x * doc_x_axis[0] + y * doc_y_axis[0]
        highlight_tlc_y = doc_y + x * doc_x_axis[1] + y * doc_y_axis[1]
        highlight_blc_x = highlight_tlc_x + height * doc_y_axis[0]
        highlight_blc_y = highlight_tlc_y + height * doc_y_axis[1]
        highlight_brc_x = highlight_blc_x + width * doc_x_axis[0]
        highlight_brc_y = highlight_blc_y + width * doc_x_axis[1]
        highlight_trc_x = highlight_tlc_x + width * doc_x_axis[0]
        highlight_trc_y = highlight_tlc_y + width * doc_x_axis[1]

        self.shape = PySI.PointVector([[highlight_tlc_x, highlight_tlc_y], [highlight_blc_x, highlight_blc_y], [highlight_brc_x, highlight_brc_y], [highlight_trc_x, highlight_trc_y]])
        self.visible = True