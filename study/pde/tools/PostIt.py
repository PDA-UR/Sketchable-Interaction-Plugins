from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.Duplicatable import Duplicatable
from plugins.study.pde.basic.Handle import Handle
from plugins.study.pde.basic.Label import Label
from plugins.study.pde.tools.Magnet import Magnet
from plugins.E import E

class PostIt(Movable, Deletable, Duplicatable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ PostIt __"
    region_display_name = "PostIt"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(PostIt, self).__init__(shape, uuid, "res/postit.png", PostIt.regiontype, PostIt.regionname, kwargs)
        self.qml_path = self.set_QML_path("PostIt.qml")
        self.color = PySI.Color(122, 252, 255, 255)

        cw, ch = self.context_dimensions()

        self.tag_offset_x = 20 * cw / 1920
        self.tag_offset_y = 10 * cw / 1080
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

        if "DRAWN" in kwargs and kwargs["DRAWN"]:
            Magnet.registered_colors.append(self.color)

        self.handles = []
        self.tags = []
        self.in_pile = False

        self.set_QML_data("text", "Post It", PySI.DataType.STRING)

        self.handle_duplication(kwargs)

        if "is_selector" not in kwargs or ("is_selector" in kwargs and not kwargs["is_selector"]):
            for i, c in enumerate(corners):
                corner = "tlc" if i == 0 else "blc" if i == 1 else "brc" if i == 2 else "trc"
                self.create_region_via_name(c, Handle.regionname, False, {"parent": self, "num": i, "corner": corner})

        pass

    def handle_duplication(self, kwargs):
        if "is_duplicate" in kwargs and kwargs["is_duplicate"]:
            self.color = kwargs["target_data"]["color"]

            self.is_duplicate = True

            for e in kwargs["qml_data"]:
                self.set_QML_data(*e)

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
            x1 = self.absolute_x_pos() + self.tag_offset_x * (i % tags_per_row + 1) + w * (i % tags_per_row) + self.handle_width
            y1 = self.absolute_y_pos() + self.height - h * (i // tags_per_row + 1) - self.tag_offset_y * (i // tags_per_row + 1)
            y_max = max(t.shape, key=lambda p: p.y).y
            y_min = min(t.shape, key=lambda p: p.y).y
            curr_h = y_max - y_min
            scale = h / curr_h
            tcenter = t.absolute_x_pos() + t.width / 2, t.absolute_y_pos() + t.height / 2
            scaled_contour = []
            for x, y in [[p.x, p.y] for p in t.shape]:
                x_scaled = (x - tcenter[0]) * scale + tcenter[0] + t.x
                y_scaled = (y - tcenter[1]) * scale + tcenter[1] + t.y
                scaled_contour.append([x_scaled, y_scaled])

            offset = scaled_contour[0]
            offset_x, offset_y = x1 - offset[0], y1 - offset[1]

            x_max = max(scaled_contour, key=lambda p: p[0])[0]
            x_min = min(scaled_contour, key=lambda p: p[0])[0]
            y_max = max(scaled_contour, key=lambda p: p[1])[1]
            y_min = min(scaled_contour, key=lambda p: p[1])[1]
            width = x_max - x_min
            height = y_max - y_min

            if t.shape_rec == "Circle":
                scaled_contour = [[p[0] + offset_x + width / 2, p[1] + offset_y] for p in scaled_contour]
            elif t.shape_rec == "Rectangle":
                scaled_contour = [[p[0] + offset_x - width / 2, p[1] + offset_y - height / 2] for p in scaled_contour]
            else:
                scaled_contour = [[p[0] + offset_x - width / 2, p[1] + offset_y + height / 2] for p in scaled_contour]

            t.shape = PySI.PointVector(scaled_contour)
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

    @SIEffect.on_enter("__RECOLOR__", SIEffect.RECEPTION)
    def on_recolor_enter_recv(self, r, g, b):
        if r is None:
            return

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
        if other.parent is self:
            if not self.is_linked(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION):
                self.create_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

            if other not in self.tags:
                self.tags.append(other)

    @SIEffect.on_leave("__ON_TAGGING_LABEL__", SIEffect.RECEPTION)
    def on_tagging_label_leave_recv(self, other):
        if other.parent is self:
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

    @SIEffect.on_enter("__ SHAPE_TAG __", SIEffect.RECEPTION)
    def on_shape_tag_enter_recv(self, tag_shape, tag_center, tag_color, tag_x, tag_y, tag_shape_recognition):
        if tag_shape is None:
            return

        w = self.width / 8
        h = self.height / 10

        tags_per_row = self.width // (self.tag_offset_x + w)

        x1 = self.absolute_x_pos() + self.tag_offset_x * (len(self.tags) % tags_per_row + 1) + w * (len(self.tags) % tags_per_row) + self.handle_width
        y1 = self.absolute_y_pos() + self.height - h * (len(self.tags) // tags_per_row + 1) - self.tag_offset_y * (len(self.tags) // tags_per_row + 1)

        self.current_height = self.height - h * (len(self.tags) // tags_per_row + 1) - self.tag_offset_y * (len(self.tags) // tags_per_row + 1)
        self.set_QML_data("height", float(self.current_height), PySI.DataType.FLOAT)

        y_max = max(tag_shape, key=lambda p: p.y).y
        y_min = min(tag_shape, key=lambda p: p.y).y
        curr_h = y_max - y_min
        scale = h / curr_h

        scaled_contour = []
        for x, y in [[p.x, p.y] for p in tag_shape]:
            x_scaled = (x - tag_center[0]) * scale + tag_center[0] + tag_x
            y_scaled = (y - tag_center[1]) * scale + tag_center[1] + tag_y
            scaled_contour.append([x_scaled, y_scaled])

        offset = scaled_contour[0]
        offset_x, offset_y = x1 - offset[0], y1 - offset[1]

        x_max = max(scaled_contour, key=lambda p: p[0])[0]
        x_min = min(scaled_contour, key=lambda p: p[0])[0]
        y_max = max(scaled_contour, key=lambda p: p[1])[1]
        y_min = min(scaled_contour, key=lambda p: p[1])[1]
        width = x_max - x_min
        height = y_max - y_min

        if tag_shape_recognition == "Circle":
            scaled_contour = [[p[0] + offset_x + width / 2, p[1] + offset_y] for p in scaled_contour]
        elif tag_shape_recognition == "Rectangle":
            scaled_contour = [[p[0] + offset_x - width / 2, p[1] + offset_y - height / 2] for p in scaled_contour]
        else:
            tag_shape_recognition = "Triangle"
            scaled_contour = [[p[0] + offset_x - width / 2, p[1] + offset_y + height / 2] for p in scaled_contour]

        self.create_region_via_name(scaled_contour, Label.regionname, False, {"parent": self, "color": tag_color, "text": "", "shape_recognition": tag_shape_recognition})

    @SIEffect.on_enter("__ DUPLICATE __", SIEffect.RECEPTION)
    def on_duplicate_enter_recv(self):
        if self.is_duplicate:
            return
        target_data = self.target_data()
        qml_data = self.qml_data(type(self))
        kwargs = {"is_duplicate": True, "target_data": target_data, "qml_data": qml_data}

        x = self.absolute_x_pos() + self.edge_round_value + self.duplicate_offset[0]
        y = self.absolute_y_pos() + self.edge_round_value + self.duplicate_offset[1]
        w = self.width - self.edge_round_value * 2
        h = self.height - self.edge_round_value * 2
        shape = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
        self.create_region_via_name(shape, self.regionname, False, kwargs)

    @SIEffect.on_enter("__ MAGNET_PULL __", SIEffect.RECEPTION)
    def on_magnet_pull_enter_recv(self, colors, shapes):
        color = [self.color.r, self.color.g, self.color.b]

        found = color in colors
        if found:
            print("FOUND1")
            return
        else:
            for t in self.tags:
                found |= t.shape_rec in shapes

        if found:
            print("FOUND2")