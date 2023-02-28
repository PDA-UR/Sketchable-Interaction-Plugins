from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


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

        self.content = []

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

            self.reshape_to_content(*self.content_dimensions())

    @SIEffect.on_leave("__PARENT_FRAME__", SIEffect.EMISSION)
    def on_parent_frame_leave_emit(self, other):
        other.remove_link(other._uuid, "__ON_RESIZED__", self._uuid, "__ON_RESIZED__")
        self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

        if other in self.content:
            self.content.remove(other)

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

    @SIEffect.on_link(SIEffect.RECEPTION, "__ON_RESIZED__", "__ON_RESIZED__")
    def on_resized_recv(self, resized, kwargs={}):
        if not resized.is_under_user_control and not resized.was_moved():
            self.reshape_to_content(*self.content_dimensions())
