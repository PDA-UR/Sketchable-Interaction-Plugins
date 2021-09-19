from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable

from plugins.E import E

class Highlight(Movable, Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.highlight_regionname
    region_display_name = E.id.highlight_region_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Highlight, self).__init__(shape, uuid, "", Highlight.regiontype, Highlight.regionname, kwargs)
        self.color = E.color.highlight_color
        self.with_border = False
        self.visible = False

        self.x_in_document = kwargs["orig_x"]
        self.y_in_document = kwargs["orig_y"]
        self.width_in_document = kwargs["orig_width"]
        self.height_in_document = kwargs["orig_height"]
        # self.orig_shape = [[p.x, p.y] for p in self.shape]

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid):
            for r in self.current_regions():
                if hasattr(r, "s_id"):
                    if len(self.linked_highlight_sids) > 0:
                        if r.s_id in self.linked_highlight_sids:
                            self.create_link(r._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

                    if r.s_id == self.c_id:
                        # self.create_link(r._uuid, E.capability.document_add_highlight, self._uuid, E.capability.document_add_highlight)
                        self.on_document_parent_document_continous_recv(*r.on_document_parent_document_continuous_emit(self))
                        # self.emit_linking_action(r._uuid, E.capability.document_add_highlight, r.on_add_highlight_link_emit())

    @SIEffect.on_continous(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid):
        for r in self.current_regions():
            if hasattr(r, "s_id"):
                if r.s_id == self.c_id:
                    self.on_document_parent_document_continous_recv(*r.on_document_parent_document_continuous_emit(self))

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        rel_x = self.x - self.last_x
        rel_y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return rel_x, rel_y, self.x, self.y

    @SIEffect.on_link(SIEffect.RECEPTION, E.capability.document_add_highlight, E.capability.document_add_highlight)
    def on_add_highlight_link_recv(self, parent_uuid): # doc_x, doc_y, width_fraction, height_fraction, doc_x_axis, doc_y_axis) -> None:
        pass
        # print("here2")


    @SIEffect.on_continous("PARENT_DOCUMENT", SIEffect.RECEPTION)
    def on_document_parent_document_continous_recv(self, doc_x, doc_y, width_fraction, height_fraction, doc_x_axis, doc_y_axis):
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

    @SIEffect.on_leave("PARENT_DOCUMENT", SIEffect.RECEPTION)
    def on_document_parent_document_leave_recv(self):
        self.delete()