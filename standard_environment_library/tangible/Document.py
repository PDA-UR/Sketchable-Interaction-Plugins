from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible

import math

class Document(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__Document__"
    region_display_name = "Document"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Document, self).__init__(shape, uuid, "res/2cm.png", Document.regiontype, Document.regionname, kwargs)
        self.color = PySI.Color(255, 0, 0, 0)
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

    @SIEffect.on_link(SIEffect.EMISSION, "ADD_HIGHLIGHT")
    def on_add_highlight_link_emit(self) -> tuple:
        return self.doc_x, self.doc_y, self.width_frac, self.height_frac, self.x_axis_normalized, self.y_axis_normalized

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    def dot(self, u, v):
        return sum((a * b) for a, b in zip(u, v))

    def vector_norm(self, v):
        return math.sqrt(self.dot(v, v))

    def normalize_vector(self, v):
        n = float(self.vector_norm(v))
        return [float(v[i]) / n for i in range(len(v))] if n != 0 else [-1 for i in range(len(v))]