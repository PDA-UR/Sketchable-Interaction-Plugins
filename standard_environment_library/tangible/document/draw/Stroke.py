from libPySI import PySI


from plugins.standard_environment_library.SIEffect import SIEffect
import math


class Stroke(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Stroke __"
    region_display_name = "Stroke"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", Stroke.regiontype, Stroke.regionname, kwargs)

        self.color = PySI.Color(255, 255, 0, 255)
        self.stroke_width = 5
        self.with_border = False
        self.orig_shape = [p for p in self.shape]
        self.length = 0
        self.transportation_path = []

        self.rebuild_shape()

    def build_shape(self):
        shape, shape_part_one, shape_part_two = [], [], []

        if len(self.transportation_path) != 0:
            p = self.transportation_path[0]
            for i in range(1, len(self.transportation_path)):
                q = self.transportation_path[i]

                pq = self.normalized_vector(self.perpendicular_vector((q[0] - p[0], q[1] - p[1])))

                shape_part_one.append([p[0] - pq[0] * (self.stroke_width / 2), p[1] - pq[1] * (self.stroke_width / 2)])
                shape_part_two.append([p[0] + pq[0] * (self.stroke_width / 2), p[1] + pq[1] * (self.stroke_width / 2)])

                p = q

            for s in shape_part_one:
                shape.append(s)

            for s in reversed(shape_part_two):
                shape.append(s)

        return shape

    def rebuild_shape(self):
        self.build_transportation_path()
        self.shape = PySI.PointVector(self.build_shape())

        self.width, self.height = self.get_region_width(), self.get_region_height()

    def perpendicular_vector(self, v):
        return -v[1], v[0]

    def normalized_vector(self, v):
        n = float(self.vector_length(v))

        if n != 0:
            return [float(v[i]) / n for i in range(len(v))]
        else:
            return [-1 for i in range(len(v))]

    def vector_length(self, v):
        return math.sqrt(self.vector_dot(v, v))

    def vector_dot(self, u, v):
        return sum((a * b) for a, b in zip(u, v))

    def build_transportation_path(self):
        self.transportation_path = []

        line = [(p.x + self.x, p.y + self.y) for p in self.orig_shape]

        prev_i = 0
        for i in range(1, len(line)):
            dx = line[i][0] - line[prev_i][0]
            dy = line[i][1] - line[prev_i][1]

            self.length += math.sqrt(dx * dx + dy * dy)
            self.transportation_path.append((line[i][0], line[i][1], self.length, line[i][0] - line[prev_i][0], line[i][1] - line[prev_i][1]))
            prev_i = i
