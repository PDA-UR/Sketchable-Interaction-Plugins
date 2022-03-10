from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
import math

class Painter(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Painter __"
    region_display_name = "Painter"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/painter.png", Painter.regiontype, Painter.regionname, kwargs)
        self.qml_path = self.set_QML_path("Painter.qml")
        self.color = PySI.Color(0, 255, 0, 255)
        self.link_partner = None
        self.with_border = False
        self.stroke_width = 14
        self.to_radians = math.pi / 180

        if "is_selector" in kwargs and kwargs["is_selector"]:
            self.delete()
            return

        if self.link_partner is None and "link_partner" in kwargs.keys() and kwargs["link_partner"] is not None:
            self.link_partner = kwargs["link_partner"]
            self.create_link(self.link_partner._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.color = kwargs["color"]
            self.link_partner.paint_tool = self
            self.original_tlc_x = self.aabb[0].x
            self.original_tlc_y = self.aabb[0].y
        else:
            self.enable_effect(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION, self.on_deletion_enter_recv, None, None)
            self.color = kwargs["color"]
            self.stroke_width = kwargs["stroke_width"]
            self.orig_shape = [p for p in self.shape]
            self.transportation_path = []
            self.length = 0
            self.rebuild_shape()

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    def on_deletion_enter_recv(self):
        pass

    @SIEffect.on_continuous("__ SET_PAINTER_STROKE_WIDTH __", SIEffect.RECEPTION)
    def on_set_painter_stroke_width_continuous_recv(self, w, is_controlled):
        if self.link_partner is not None:
            if w != self.stroke_width and is_controlled:
                self.color = PySI.Color(255, 0, 0, 255)
                shape = []
                cx, cy = self.absolute_x_pos() + (self.aabb[3].x - self.aabb[0].x) / 2, self.absolute_y_pos() + (self.aabb[1].y - self.aabb[0].y) / 2

                for i in range(360):
                    x, y = w / 2 * math.cos(i * self.to_radians) + cx, w / 2 * math.sin(i * self.to_radians) + cy
                    shape.append([x, y])

                self.shape = PySI.PointVector(shape)
                self.width = int(self.aabb[3].x - self.aabb[0].x)
                self.height = int(self.aabb[1].y - self.aabb[0].y)
                self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
                self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)
                ncx, ncy = self.absolute_x_pos() + (self.aabb[3].x - self.aabb[0].x) / 2, self.absolute_y_pos() + (self.aabb[1].y - self.aabb[0].y) / 2
                self.move(self.x - (ncx - cx), self.y - (ncy - cy))
                self.stroke_width = w

    def rebuild_shape(self):
        self.build_transportation_path()
        self.shape = PySI.PointVector(self.build_shape())
        self.width, self.height = self.get_region_width(), self.get_region_height()

    def build_transportation_path(self):
        self.transportation_path = []
        line = [(p.x + self.x, p.y + self.y) for p in self.orig_shape]
        for i in range(len(line)):
            self.transportation_path.append((line[i][0], line[i][1]))

    def build_shape(self):
        shape, shape_part_one, shape_part_two = [], [], []

        if len(self.transportation_path) != 0:
            p = self.transportation_path[0]
            for i in range(1, len(self.transportation_path)):
                q = self.transportation_path[i]
                pq = self.normalize_vector(self.perpendicular_vector((q[0] - p[0], q[1] - p[1])))
                shape_part_one.append([p[0] - pq[0] * (self.stroke_width / 2), p[1] - pq[1] * (self.stroke_width / 2)])
                shape_part_two.append([p[0] + pq[0] * (self.stroke_width / 2), p[1] + pq[1] * (self.stroke_width / 2)])
                p = q

            for s in shape_part_one:
                shape.append(s)

            for s in reversed(shape_part_two):
                shape.append(s)

        return shape

    def perpendicular_vector(self, v):
        return -v[1], v[0]

    def normalize_vector(self, v):
        n = float(self.vector_norm(v))
        return [float(v[i]) / n for i in range(len(v))] if n != 0 else [-1 for i in range(len(v))]

    def vector_norm(self, v):
        return math.sqrt(self.dot(v, v))

    def dot(self, u, v):
        return sum((a * b) for a, b in zip(u, v))

