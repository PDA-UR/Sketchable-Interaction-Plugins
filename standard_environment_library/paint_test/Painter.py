from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
import math
from scipy.interpolate import splprep, splev
import splines
import numpy as np

class Painter(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Painter __"
    region_display_name = "Painter"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/painter.png", Painter.regiontype, Painter.regionname, kwargs)
        cw, ch = self.context_dimensions()
        self.color = PySI.Color(0, 255, 0, 255)
        self.link_partner = None
        self.with_border = False
        self.stroke_width = 2 * cw / 1920
        self.to_radians = math.pi / 180
        self.is_tool = False

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
            self.is_tool = True
            self.move(self.x + self.stroke_width / 2, self.y + self.stroke_width / 2)
        else:
            self.enable_effect(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION, self.on_deletion_enter_recv, None, None)
            self.color = kwargs["color"]
            self.stroke_width = kwargs["stroke_width"]
            self.orig_shape = [p for p in self.shape]
            self.transportation_path = []
            self.rebuild_shape()
            self.is_tool = False

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        if not self.is_tool:
            super().on_deletion_enter_recv()

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_continuous_recv(self):
        if not self.is_tool:
            super().on_deletion_enter_recv()

    @SIEffect.on_continuous("__RECOLOR__", SIEffect.RECEPTION)
    def on_recolor_continuous_recv(self, r, g, b):
        self.color = PySI.Color(r, g, b, 255)

    @SIEffect.on_enter("__RECOLOR__", SIEffect.RECEPTION)
    def on_recolor_enter_recv(self, r, g, b):
        if r is None:
            return

        self.color = PySI.Color(r, g, b, 255)

    @SIEffect.on_continuous("__ SET_PAINTER_STROKE_WIDTH __", SIEffect.RECEPTION)
    def on_set_painter_stroke_width_continuous_recv(self, w, is_controlled):
        if self.link_partner is not None:
            if w != self.stroke_width and is_controlled:
                shape = []
                cx, cy = self.absolute_x_pos() + (self.aabb[3].x - self.aabb[0].x) / 2, self.absolute_y_pos() + (self.aabb[1].y - self.aabb[0].y) / 2

                for i in range(360):
                    x, y = w / 2 * math.cos(i * self.to_radians) + cx, w / 2 * math.sin(i * self.to_radians) + cy
                    shape.append([x + self.width / 2, y + self.height / 2])

                self.shape = PySI.PointVector(shape)
                self.width = int(self.aabb[3].x - self.aabb[0].x)
                self.height = int(self.aabb[1].y - self.aabb[0].y)
                self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
                self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)
                ncx, ncy = self.absolute_x_pos() + self.width / 2, self.absolute_y_pos() + self.height / 2
                self.move(self.x - (ncx - cx), self.y - (ncy - cy))
                self.stroke_width = w

    def rebuild_shape(self):
        self.build_transportation_path()
        self.shape = PySI.PointVector(self.build_shape())
        self.width, self.height = self.get_region_width(), self.get_region_height()

    def build_transportation_path(self):
        self.transportation_path = []
        line = [(p.x + self.x, p.y + self.y) for p in self.orig_shape]
        prev_i = 0
        self.transportation_path.append((int(line[0][0]), int(line[0][1])))
        for i in range(len(line)):
            dx = line[i][0] - line[prev_i][0]
            dy = line[i][1] - line[prev_i][1]
            if math.sqrt(dx * dx + dy * dy) > 15:
                self.transportation_path.append((int(line[i][0]), int(line[i][1])))
                prev_i = i
        self.transportation_path.append((int(line[-1][0]), int(line[-1][1])))

    def build_shape(self):
        if self.shape_recognition != "":
            shape = [[p.x, p.y] for p in self.orig_shape]

            return shape


        shape, shape_part_one, shape_part_two = [], [], []

        if len(self.transportation_path) != 0:
            p = self.transportation_path[0]
            q = self.transportation_path[1]
            qp = self.normalize_vector((p[0] - q[0], p[1] - q[1]))

            self.transportation_path.insert(0, (p[0] + qp[0] * self.stroke_width / 2, p[1] + qp[1] * self.stroke_width / 2))

            p = self.transportation_path[0]
            for i in range(1, len(self.transportation_path)):
                q = self.transportation_path[i]
                pq = self.normalize_vector(self.perpendicular_vector((q[0] - p[0], q[1] - p[1])))
                shape_part_one.append([p[0] - pq[0] * (self.stroke_width / 2), p[1] - pq[1] * (self.stroke_width / 2)])
                shape_part_two.append([p[0] + pq[0] * (self.stroke_width / 2), p[1] + pq[1] * (self.stroke_width / 2)])
                p = q

            shape_part_one = self.compute_spline_points(shape_part_one)
            shape_part_two = self.compute_spline_points(shape_part_two)

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

    def compute_spline_points(self, points: list) -> list:
        spline = splines.CatmullRom(points)
        dots_per_second = 20
        total_duration = spline.grid[-1] - spline.grid[0]
        dots = int(total_duration * dots_per_second) + 1
        times = spline.grid[0] + np.arange(dots) / dots_per_second
        result = spline.evaluate(times).T

        return [[result[0][i], result[1][i]] for i in range(len(result[0]))]

    @SIEffect.on_enter("__ SHAPE_TAG __", SIEffect.EMISSION)
    def on_shape_tag_enter_emit(self, other):
        if self.is_tool or self.shape_recognition == "":
            return None, None, None, None, None, None

        return self.shape, (self.absolute_x_pos() + self.width / 2, self.absolute_y_pos() + self.height / 2), self.color, self.x, self.y, self.shape_recognition

    @SIEffect.on_enter("__RECOLOR__", SIEffect.EMISSION)
    def on_recolor_enter_emit(self, other):
        if not self.is_tool:
            return None, None, None

        return self.color.r, self.color.g, self.color.b