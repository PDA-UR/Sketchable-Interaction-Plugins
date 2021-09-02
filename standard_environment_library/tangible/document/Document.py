from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library.tangible.document.tools.Color import Color

from plugins.E import E

import math

class Document(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.document_regionname
    region_display_name = E.id.document_region_display_name

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str="", kwargs: dict = {}) -> None:
        super(Document, self).__init__(shape, uuid, E.id.document_texture, Document.regiontype, Document.regionname, kwargs)
        self.color = E.color.document_color
        self.original_doc_width = 595.446
        self.original_doc_height = 841.691
        self.with_border = True

        self.doc_width = kwargs["width"]
        self.doc_height = kwargs["height"]

        self.width_frac = self.doc_width / self.original_doc_width
        self.height_frac = self.doc_height / self.original_doc_height
        self.doc_x = kwargs["x"]
        self.doc_y = kwargs["y"]
        self.x_axis_normalized = kwargs["x_axis"]
        self.y_axis_normalized = kwargs["y_axis"]

    @SIEffect.on_link(SIEffect.EMISSION, E.capability.document_add_highlight)
    def on_add_highlight_link_emit(self) -> tuple:
        return self.doc_x, self.doc_y, self.width_frac, self.height_frac, self.x_axis_normalized, self.y_axis_normalized

    @SIEffect.on_continuous("PARENT_DOCUMENT", SIEffect.EMISSION)
    def on_document_parent_document_continuous_emit(self, other):
        pass

    @SIEffect.on_leave("PARENT_DOCUMENT", SIEffect.EMISSION)
    def on_document_parent_document_leave_emit(self, other):
        pass

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass