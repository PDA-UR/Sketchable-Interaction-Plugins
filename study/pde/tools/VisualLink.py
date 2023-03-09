from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
import math


class VisualLink(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ VisualLink __"
    region_display_name = "VisualLink"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(VisualLink, self).__init__(shape, uuid, "res/link.png", VisualLink.regiontype, VisualLink.regionname, kwargs)
        self.color = PySI.Color(100, 100, 100, 255)
        self.border_color = PySI.Color(100, 100, 100, 255)
        self.is_visually_linked = False

        if not "linked" in kwargs.keys() or not kwargs["linked"]:
            self.targets = []
        elif "linked" in kwargs.keys() and kwargs["linked"]:
            self.start = None
            self.end = None
            self.is_visually_linked = True
            self.initial_reshape = True
            self.stroke_width = 3
            self.transportation_path = []
            self.start = kwargs["targets"][0]
            self.end = kwargs["targets"][1]
            self.build_link()

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        if self.is_visually_linked:
            self.disable_effect("__ON_VISUAL_LINK__", SIEffect.EMISSION)

    @SIEffect.on_enter("__ON_VISUAL_LINK__", SIEffect.EMISSION)
    def on_visual_link_enter_emit(self, other):
        if not self.is_visually_linked:
            if other not in self.targets:
                self.targets.append(other)

    @SIEffect.on_continuous("__ON_VISUAL_LINK__", SIEffect.EMISSION)
    def on_visual_link_continuous_emit(self, other):
        if not self.is_visually_linked:
            if len(self.targets) > 1:
                targets = self.targets[0], self.targets[-1]
                self.create_region_via_name(self.shape, VisualLink.regionname, False, {"linked": True, "targets": targets})
                self.targets = []
                self.delete()

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y, kwargs={}):
        super().set_position_from_position(rel_x, rel_y, abs_x, abs_y)
        if (rel_x > 0 or rel_y > 0) or self.initial_reshape:
            self.reshape()
            self.initial_reshape = False

            self.x = 0
            self.y = 0
            self.last_x = 0
            self.last_y = 0

    @SIEffect.on_link(SIEffect.RECEPTION, "__ON_RESIZED__", "__ON_RESIZED__")
    def on_resized_recv(self, resized, kwargs={}):
        self.reshape()

    def reshape(self):
        scx = self.start.aabb[0].x + self.start.width / 2 + self.start.x
        ecx = self.end.aabb[0].x + self.end.width / 2 + self.end.x
        scy = self.start.aabb[0].y + self.start.height / 2 + self.start.y
        ecy = self.end.aabb[0].y + self.end.height / 2 + self.end.y

        start_shape = [[p.x + self.start.x, p.y + self.start.y] for p in self.start.shape] + [[self.start.shape[len(self.start.shape) - 1].x + self.start.x, self.start.shape[len(self.start.shape) - 1].y + self.start.y]]
        end_shape = [[p.x + self.end.x, p.y + self.end.y] for p in self.end.shape] + [[self.end.shape[len(self.end.shape) - 1].x + self.end.x, self.end.shape[len(self.end.shape) - 1].y + self.end.y]]

        sq = self.intersect([scx, scy], [ecx, ecy], start_shape)
        eq = self.intersect([scx, scy], [ecx, ecy], end_shape)

        if sq is not None and eq is not None:
            self.orig_shape = [p for p in PySI.PointVector([[sq[0], sq[1]], [eq[0], eq[1]]])]
            self.rebuild_shape()

    def build_link(self):
        self.start.create_link(self.start._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.start.create_link(self.start._uuid, "__ON_RESIZED__", self._uuid, "__ON_RESIZED__")
        self.start.create_link(self.end._uuid, "__ON_RESIZED__", self._uuid, "__ON_RESIZED__")
        self.start.create_link(self.start._uuid, PySI.LinkingCapability.POSITION, self.end._uuid, PySI.LinkingCapability.POSITION)
        self.start.create_link(self.end._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

        self.reshape()

    def intersect(self, s, e, shape):
        for i in range(len(shape) - 1):
            q = self.line_intersection([[s[0], s[1]], [e[0], e[1]]], [[shape[i][0], shape[i][1]], [shape[i + 1][0], shape[i + 1][1]]])
            if q is not None:
                return q

        return None

    @SIEffect.on_continuous("__RECOLOR__", SIEffect.RECEPTION)
    def on_recolor_continuous_emit(self, r, g, b):
        self.color = PySI.Color(r, g, b, 255)
        self.border_color = PySI.Color(r, g, b, 255)

    def line_intersection(self, line1, line2):
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        # Calculate the denominator of the equations
        denominator = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))

        # If the denominator is 0, the lines are parallel
        if denominator == 0:
            return None

        # Calculate the numerators of the equations
        numerator1 = ((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))
        numerator2 = ((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))

        # Calculate the u and v parameters
        u = numerator1 / denominator
        v = numerator2 / denominator

        # Check if the intersection is within the line segments
        if u < 0 or u > 1 or v < 0 or v > 1:
            return None

        # Calculate the intersection point
        x = x1 + (u * (x2 - x1))
        y = y1 + (u * (y2 - y1))

        return x, y

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
        import splines
        import numpy as np
        spline = splines.CatmullRom(points)
        dots_per_second = 20
        total_duration = spline.grid[-1] - spline.grid[0]
        dots = int(total_duration * dots_per_second) + 1
        times = spline.grid[0] + np.arange(dots) / dots_per_second
        result = spline.evaluate(times).T

        return [[result[0][i], result[1][i]] for i in range(len(result[0]))]

    def interpolate(self, pts):
        import numpy as np
        from scipy.interpolate import splprep, splev

        X = np.array([p[0] for p in pts])
        Y = np.array([p[1] for p in pts])
        pts = np.vstack((X, Y))
        # Find the B-spline representation of an N-dimensional curve
        tck, u = splprep(pts, s=0.0)
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new = splev(u_new, tck)

        return [[x, y] for x, y in zip(x_new, y_new)]


