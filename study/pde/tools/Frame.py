from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
import math

class Frame(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Frame __"
    region_display_name = "Frame"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Frame, self).__init__(shape, uuid, "res/frame.png", Frame.regiontype, Frame.regionname, kwargs)
        self.color = PySI.Color(0, 0, 0, 0)
        self.qml_path = self.set_QML_path("Frame.qml")

        cw, ch = self.context_dimensions()

        self.border_width = int(4 * cw / 1920)
        self.title_offset = int(50 * ch / 1080)

        self.shape = PySI.PointVector(self.round_edge([
            [self.aabb[0].x, self.aabb[0].y],
            [self.aabb[1].x, self.aabb[1].y],
            [self.aabb[2].x, self.aabb[2].y],
            [self.aabb[3].x, self.aabb[3].y]
        ]))

        self.pile_factor = 0.95
        self.scatter_factor = 1 // (1 - 0.95)
        self.unpiled_center = (0, 0)

        self.content = []
        self.is_piled = False

        self.set_QML_data("width", float(self.width), PySI.DataType.FLOAT)
        self.set_QML_data("height", float(self.title_offset), PySI.DataType.FLOAT)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_continuous("__RECOLOR__", SIEffect.RECEPTION)
    def on_recolor_continuous_recv(self, r, g, b):
        self.border_color = PySI.Color(r, g, b, 255)
        self.default_border_color = PySI.Color(r, g, b, 255)

    @SIEffect.on_continuous("__PARENT_FRAME__", SIEffect.EMISSION)
    def on_parent_frame_continuous_emit(self, other):
        if not other.is_under_user_control and other.was_moved():
            if other not in self.content:
                self.content.append(other)
                other.create_link(other._uuid, "__ON_RESIZED__", self._uuid, "__ON_RESIZED__")
                self.create_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_leave("__PARENT_FRAME__", SIEffect.EMISSION)
    def on_parent_frame_leave_emit(self, other):
        other.remove_link(other._uuid, "__ON_RESIZED__", self._uuid, "__ON_RESIZED__")
        self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

        if other in self.content:
            self.content.remove(other)

    def on_double_clicked(self):
        if len(self.content) == 0:
            self.is_piled = False
            return

        if self.is_piled == False:
            self.pile()
        else:
            self.scatter()

        self.is_piled = not self.is_piled

    def pile(self):
        scenterx, scentery = self.absolute_x_pos() + self.width / 2, self.absolute_y_pos() + self.height / 2 + self.title_offset
        self.unpiled_center = scenterx, scentery

        for c in self.content:
            centerx, centery = c.absolute_x_pos() + c.width / 2, c.absolute_y_pos() + c.height / 2

            v = scenterx - centerx, scentery - centery
            vl = self.vector_norm(v) * self.pile_factor
            v = self.normalize_vector(v)
            v = v[0] * vl, v[1] * vl
            c.in_pile = True
            c.move(c.x + v[0], c.y + v[1])

        self.reshape_to_content(*self.content_dimensions())

    def scatter(self):
        scenterx, scentery = self.unpiled_center[0], self.unpiled_center[1]

        for c in self.content:
            centerx, centery = c.absolute_x_pos() + c.width / 2, c.absolute_y_pos() + c.height / 2

            v = centerx - scenterx, centery - scentery
            vl = self.vector_norm(v) * self.scatter_factor
            v = self.normalize_vector(v)
            v = v[0] * vl, v[1] * vl

            if c.in_pile:
                c.move(c.x + v[0], c.y + v[1])
            c.in_pile = False

        self.reshape_to_content(*self.content_dimensions())

    def content_dimensions(self):
        if len(self.content) > 0:
            tlc = self.content[0].absolute_x_pos(), self.content[0].absolute_y_pos()
            brc = self.content[0].absolute_x_pos() + self.content[0].width, self.content[0].absolute_y_pos() + self.content[0].height

        for c in self.content:
            tlc = min(tlc[0], c.absolute_x_pos()), min(tlc[1], c.absolute_y_pos())
            brc = max(brc[0], c.absolute_x_pos() + c.width), max(brc[1], c.absolute_y_pos() + c.height)

        return tlc, (tlc[0], brc[1]), brc, (brc[0], tlc[1])

    def reshape_to_content(self, tlc, blc, brc, trc):
        self.shape = PySI.PointVector(self.round_edge([
            [tlc[0], tlc[1] - self.title_offset],
            [blc[0], blc[1]],
            [brc[0], brc[1]],
            [trc[0], trc[1] - self.title_offset]
        ]))

        self.x = 0
        self.y = 0
        self.last_x = 0
        self.last_y = 0

        self.width = int(self.aabb[3].x - self.aabb[0].x)
        self.height = int(self.aabb[1].y - self.aabb[0].y)

        self.set_QML_data("width", float(self.width), PySI.DataType.FLOAT)
        self.set_QML_data("height", float(self.title_offset), PySI.DataType.FLOAT)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y, {"moved_by_target": True}

    @SIEffect.on_continuous("__ FRAME_MERGE __", SIEffect.EMISSION)
    def on_frame_merge_continuous_emit(self, other):
        if self.was_moved():
            self.delete()
            return self._uuid, self.content

        return self._uuid, None

    @SIEffect.on_continuous("__ FRAME_MERGE __", SIEffect.RECEPTION)
    def on_frame_merge_continuous_recv(self, other_uuid, other_tags=None):
        if self.is_under_user_control or self.was_moved() or other_tags is None:
            return

        for c in other_tags:
            c.remove_link(other_uuid, PySI.LinkingCapability.POSITION, c._uuid, PySI.LinkingCapability.POSITION)
            c.remove_link(c._uuid, "__ON_RESIZED__", self._uuid, "__ON_RESIZED__")

            self.content.append(c)
            c.create_link(c._uuid, "__ON_RESIZED__", self._uuid, "__ON_RESIZED__")
            self.create_link(self._uuid, PySI.LinkingCapability.POSITION, c._uuid, PySI.LinkingCapability.POSITION)

        ctlc, cblc, cbrc, ctrc = self.content_dimensions()

        cleftx = min(ctlc[0], cblc[0])
        crightx = max(ctrc[0], cbrc[0])

        ctopy = min(ctlc[1], ctrc[1])
        cbottomy = max(cblc[1], cbrc[1])

        stlcx, stlcy = self.absolute_x_pos(), self.absolute_y_pos()
        stlc, sblc, sbrc, strc = (stlcx, stlcy), (stlcx, stlcy + self.height), (stlcx + self.width, stlcy + self.height), (stlcx + self.width, stlcy)

        leftx = stlcx if stlcx < cleftx else cleftx
        topy = stlcy if stlcy < ctopy else ctopy
        rightx = strc[0] if strc[0] > crightx else crightx
        bottomy = sblc[1] if sblc[1] > cbottomy else cbottomy

        tlc, blc, brc, trc = (leftx + self.edge_round_value, topy + self.edge_round_value + self.title_offset), (leftx + self.edge_round_value, bottomy - self.edge_round_value), (rightx - self.edge_round_value, bottomy - self.edge_round_value), (rightx - self.edge_round_value, topy + self.edge_round_value + self.title_offset)

        self.reshape_to_content(tlc, blc, brc, trc)

    def perpendicular_vector(self, v):
        return -v[1], v[0]

    def normalize_vector(self, v):
        n = float(self.vector_norm(v))
        return [float(v[i]) / n for i in range(len(v))] if n != 0 else [-1 for i in range(len(v))]

    def vector_norm(self, v):
        return math.sqrt(self.dot(v, v))

    def dot(self, u, v):
        return sum((a * b) for a, b in zip(u, v))