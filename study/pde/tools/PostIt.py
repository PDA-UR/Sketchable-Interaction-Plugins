from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.study.pde.basic.Handle import Handle
from plugins.study.pde.basic.Label import Label
from plugins.E import E


class PostIt(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ PostIt __"
    region_display_name = "PostIt"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(PostIt, self).__init__(shape, uuid, "res/postit.png", PostIt.regiontype, PostIt.regionname, kwargs)
        self.qml_path = self.set_QML_path("PostIt.qml")
        self.color = PySI.Color(122, 252, 255, 255)
        cw, ch = self.context_dimensions()
        self.tag_offset_x = 15 * cw / 1920
        self.tag_offset_y = 5 * cw / 1080
        self.handle_width = 20 * cw / 1920
        self.current_height = self.height

        x1 = self.aabb[0].x
        y1 = self.aabb[0].y
        x2 = self.aabb[2].x - self.handle_width
        y2 = self.aabb[2].y - self.handle_width

        corners = [
            PySI.PointVector([[x1, y1], [x1, y1 + self.handle_width], [x1 + self.handle_width, y1 + self.handle_width], [x1 + self.handle_width, y1]]),
            PySI.PointVector([[x1, y2], [x1, y2 + self.handle_width], [x1 + self.handle_width, y2 + self.handle_width], [x1 + self.handle_width, y2]]),
            PySI.PointVector([[x2, y2], [x2, y2 + self.handle_width], [x2 + self.handle_width, y2 + self.handle_width], [x2 + self.handle_width, y2]]),
            PySI.PointVector([[x2, y1], [x2, y1 + self.handle_width], [x2 + self.handle_width, y1 + self.handle_width], [x2 + self.handle_width, y1]])
        ]

        self.handles = []
        self.tags = []

        if "is_selector" not in kwargs or ("is_selector" in kwargs and not kwargs["is_selector"]):
            for i, c in enumerate(corners):
                corner = "tlc" if i == 0 else "blc" if i == 1 else "brc" if i == 2 else "trc"
                self.create_region_via_name(c, Handle.regionname, False, {"parent": self, "num": i, "corner": corner})

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y, {"moved_by_target": True}

    @SIEffect.on_link(SIEffect.RECEPTION, "__RESIZE__", "__RESIZE__")
    def resize(self, num, kwargs={}):
        if len(self.handles) < 4:
            return

        affectedx, affectedy = self.get_affected_corners(num)
        self.handles[affectedx].x = self.handles[num].x
        self.handles[affectedy].y = self.handles[num].y

        self.reshape_according_to_resize()

        self.set_QML_data("width", float(self.width), PySI.DataType.FLOAT)
        self.set_QML_data("height", float(self.current_height), PySI.DataType.FLOAT)

        self.emit_linking_action(self._uuid, "__ON_RESIZED__", self.on_resized_emit())

    def reshape_according_to_resize(self):
        self.shape = PySI.PointVector(self.round_edge([
            [self.handles[0].aabb[0].x + self.handles[0].x, self.handles[0].y + self.handles[0].aabb[0].y],
            [self.handles[1].aabb[0].x + self.handles[0].x, self.handles[1].y + self.handles[1].aabb[1].y],
            [self.handles[2].aabb[3].x + self.handles[3].x, self.handles[2].y + self.handles[2].aabb[1].y],
            [self.handles[3].aabb[3].x + self.handles[3].x, self.handles[3].y + self.handles[3].aabb[0].y]
        ]))

        w = self.width / 8
        h = self.height / 10

        tags_per_row = self.width // (self.tag_offset_x + w)
        for i, t in enumerate(self.tags):
            x = self.aabb[0].x + self.tag_offset_x * (i % tags_per_row + 1) + w * (i % tags_per_row) + self.handle_width
            y = self.aabb[0].y + self.height - h * (i // tags_per_row + 1) - self.tag_offset_y * (i // tags_per_row + 1)

            self.set_QML_data("height", float(self.current_height), PySI.DataType.FLOAT)

            t.shape = PySI.PointVector([
                [x, y],
                [x, y + h],
                [x + w, y + h],
                [x + w, y]
            ])

            t.width = int(t.aabb[3].x - t.aabb[0].x)
            t.height = int(t.aabb[1].y - t.aabb[0].y)

            t.x = 0
            t.y = 0
            t.last_x = 0
            t.last_y = 0

            t.set_QML_data("width", float(t.width), PySI.DataType.FLOAT)
            t.set_QML_data("height", float(t.height), PySI.DataType.FLOAT)

        self.x = 0
        self.y = 0
        self.last_x = 0
        self.last_y = 0

        self.width = int(self.aabb[3].x - self.aabb[0].x)
        self.height = int(self.aabb[1].y - self.aabb[0].y)
        self.current_height = self.height - h * (len(self.tags) // tags_per_row + 1) - self.tag_offset_y * (len(self.tags) // tags_per_row + 1)

    def get_affected_corners(self, source):
        if source == 0: #tlc
            return 1, 3
        if source == 1: #blc
            return 0, 2
        if source == 2: #brc
            return 3, 1
        if source == 3: #trc
            return 2, 0

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_link(SIEffect.EMISSION, "__ON_RESIZED__")
    def on_resized_emit(self):
        return self, {}

    @SIEffect.on_continuous("__RECOLOR__", SIEffect.RECEPTION)
    def on_recolor_continuous_recv(self, r, g, b):
        if self.color.r == r and self.color.g == g and self.color.b == b:
            return

        self.color = PySI.Color(r, g, b, 255)

    @SIEffect.on_continuous("__PARENT_FRAME__", SIEffect.RECEPTION)
    def on_parent_frame_continuous_recv(self):
        pass

    @SIEffect.on_leave("__PARENT_FRAME__", SIEffect.RECEPTION)
    def on_parent_frame_leave_recv(self):
        pass

    @SIEffect.on_enter("__ON_TAGGING__", SIEffect.RECEPTION)
    def on_tagging_enter_recv(self, color, text):
        w = self.width / 8
        h = self.height / 10

        tags_per_row = self.width // (self.tag_offset_x + w)

        x = self.absolute_x_pos() + self.tag_offset_x * (len(self.tags) % tags_per_row + 1) + w * (len(self.tags) % tags_per_row) + self.handle_width
        y = self.absolute_y_pos() + self.height - h * (len(self.tags) // tags_per_row + 1) - self.tag_offset_y * (len(self.tags) // tags_per_row + 1)

        self.current_height = self.height - h * (len(self.tags) // tags_per_row + 1) - self.tag_offset_y * (len(self.tags) // tags_per_row + 1)

        self.set_QML_data("height", float(self.current_height), PySI.DataType.FLOAT)

        s = PySI.PointVector([
            [x, y],
            [x, y + h],
            [x + w, y + h],
            [x + w, y]
        ])

        self.create_region_via_name(s, Label.regionname, False, {"parent": self, "color": color, "text": text})

    @SIEffect.on_enter("__ON_TAGGING_LABEL__", SIEffect.RECEPTION)
    def on_tagging_label_enter_recv(self, other):
        if not self.is_linked(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION):
            self.create_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

        if other not in self.tags:
            self.tags.append(other)

    @SIEffect.on_leave("__ON_TAGGING_LABEL__", SIEffect.RECEPTION)
    def on_tagging_label_leave_recv(self, other):
        if other.is_under_user_control:
            self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

            if other in self.tags:
                self.tags.remove(other)

            w = self.width / 8
            h = self.height / 10
            tags_per_row = self.width // (self.tag_offset_x + w)

            self.current_height = self.height - h * (len(self.tags) // tags_per_row + 1) - self.tag_offset_y * (len(self.tags) // tags_per_row + 1)

            self.set_QML_data("height", float(self.current_height), PySI.DataType.FLOAT)

    @SIEffect.on_enter("__ON_VISUAL_LINK__", SIEffect.RECEPTION)
    def on_visual_link_enter_recv(self):
        pass

    @SIEffect.on_continuous("__ON_VISUAL_LINK__", SIEffect.RECEPTION)
    def on_visual_link_continuous_recv(self):
        pass

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        for h in self.handles:
            h.flagged_for_deletion = True
            h.delete()

        for t in self.tags:
            t.flagged_for_deletion = True
            t.delete()
        super().on_deletion_enter_recv()

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_continuous_recv(self):
        for h in self.handles:
            h.flagged_for_deletion = True
            h.delete()

        for t in self.tags:
            t.flagged_for_deletion = True
            t.delete()
        super().on_deletion_enter_recv()
