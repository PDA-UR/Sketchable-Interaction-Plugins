from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E

import math
import time


class ConveyorBelt(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ ConveyorBelt __"
    region_display_name = "ConveyorBelt"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        Deletable.__init__(self, shape, uuid, "res/factory.png", ConveyorBelt.regiontype, ConveyorBelt.regionname, kwargs)
        Movable.__init__(self, shape, uuid, "res/factory.png", ConveyorBelt.regiontype, ConveyorBelt.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, "res/factory.png", ConveyorBelt.regiontype, ConveyorBelt.regionname, kwargs)

        self.qml_path = self.set_QML_path("ConveyorBelt.qml")
        self.color = PySI.Color(204, 255, 204, 255)

        self.conveyor_point_step = 1
        self.conveyor_width = E.id.cb_width

        self.length = 0
        self.speed = 250

        self.delta_x = 0
        self.delta_y = 0

        self.collision_pixel_variance = 7
        self.transportation_path_changed = False

        # will contain tuples of (item_x, item_y, overall length up to this point, distance_x_to_prev_point, distance_y_to_prev_point
        self.transportation_path = []
        self.rebuild_shape()

    def build_transportation_path(self):
        line = [(p.x, p.y) for p in self.shape]

        prev_i = 0
        for i in range(1, len(line), self.conveyor_point_step):
            dx = line[i][0] - line[prev_i][0]
            dy = line[i][1] - line[prev_i][1]

            if math.sqrt(dx * dx + dy * dy) > 5:
                self.length += math.sqrt(dx * dx + dy * dy)
                self.transportation_path.append((line[i][0], line[i][1], self.length, line[i][0] - line[prev_i][0], line[i][1] - line[prev_i][1]))
                prev_i = i

        self.transportation_path = self.transportation_path[2:-2]

    def build_shape(self):
        shape, shape_part_one, shape_part_two = [], [], []

        if len(self.transportation_path) != 0:
            p = self.transportation_path[0]
            for i in range(1, len(self.transportation_path), self.conveyor_point_step):
                q = self.transportation_path[i]

                pq = self.normalized_vector(self.perpendicular_vector((q[0] - p[0], q[1] - p[1])))

                shape_part_one.append([p[0] - pq[0] * (self.conveyor_width / 2), p[1] - pq[1] * (self.conveyor_width / 2)])
                shape_part_two.append([p[0] + pq[0] * (self.conveyor_width / 2), p[1] + pq[1] * (self.conveyor_width / 2)])

                p = q

            for s in shape_part_one:
                shape.append(s)

            for s in reversed(shape_part_two):
                shape.append(s)

        return shape

    def rebuild_shape(self):
        self.build_transportation_path()

        self.shape = PySI.PointVector(self.build_shape())

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

    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        return x, y

    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        super(ConveyorBelt, self).set_position_from_position(rel_x, rel_y, abs_x, abs_y)

        self.delta_x, self.delta_y = rel_x, rel_y

        self.transportation_path_changed = True

        for i in range(len(self.transportation_path)):
            self.transportation_path[i] = self.transportation_path[i][0] + rel_x, self.transportation_path[i][1] + rel_y, self.transportation_path[i][2]

    def compute_conveyor_belt_item_insertion_position(self, other):
        target_segment_start_point_index = -1
        smallest_distance = 99999
        q = other.x + other.width / 2, other.y + other.height / 2  # use middle points of other

        for i, p in enumerate(self.transportation_path):
            r = q[0] - p[0], q[1] - p[1]

            distance = self.vector_length(r)

            if distance < smallest_distance:
                smallest_distance = distance
                target_segment_start_point_index = i

        return target_segment_start_point_index

    @SIEffect.on_enter(E.id.transportable_capability, SIEffect.EMISSION)
    def on_transport_enter_emit(self, item):
        segment_start_index = self.compute_conveyor_belt_item_insertion_position(item)
        segment_start_index = 1 if segment_start_index == 0 else segment_start_index
        distance = 0
        specific_path = []

        if self.transportation_path[segment_start_index] != (item.x, item.y):
            for i in range(segment_start_index, len(self.transportation_path)):
                distance += self.vector_length((self.transportation_path[i][0] - self.transportation_path[i - 1][0], self.transportation_path[i][1] - self.transportation_path[i - 1][1]))
                specific_path.append((self.transportation_path[i][0], self.transportation_path[i][1], distance))

        return self.transportation_path[segment_start_index][0], self.transportation_path[segment_start_index][1], distance, specific_path

    @SIEffect.on_continuous(E.id.transportable_capability, SIEffect.EMISSION)
    def on_transport_continuous_emit(self, item):
        if self.transportation_path_changed:
            self.transportation_path_changed = False

            for i in range(len(item.transportation_path)):
                item.transportation_path[i] = item.transportation_path[i][0] + self.delta_x, item.transportation_path[i][1] + self.delta_y, item.transportation_path[i][2]

        if item.is_under_user_control:
            segment_start_index = self.compute_conveyor_belt_item_insertion_position(item)
            segment_start_index = 1 if segment_start_index == 0 else segment_start_index
            distance = 0
            specific_path = []

            if self.transportation_path[segment_start_index] != (item.x, item.y):
                for i in range(segment_start_index, len(self.transportation_path)):
                    distance += self.vector_length((self.transportation_path[i][0] - self.transportation_path[i - 1][0], self.transportation_path[i][1] - self.transportation_path[i - 1][1]))
                    specific_path.append((self.transportation_path[i][0], self.transportation_path[i][1], distance))

                item.transportation_path = specific_path
                item.overall_transportation_length = distance
                item.transportation_starttime = time.time()

            return item.x, item.y, False

        t = time.time() - item.transportation_starttime

        distance = (t * self.speed) % item.overall_transportation_length

        for i in range(1, len(item.transportation_path)):
            if i < len(item.transportation_path) - 1:
                if distance < item.transportation_path[i][2]:
                    p_from = item.transportation_path[i - 1]
                    p_to = item.transportation_path[i]
                    f = (distance - p_from[2]) / (p_to[2] - p_from[2])

                    x = p_from[0] + (p_to[0] - p_from[0]) * f
                    y = p_from[1] + (p_to[1] - p_from[1]) * f

                    return x, y, False

        return item.transportation_path[-1][0], item.transportation_path[-1][1], True

    @SIEffect.on_leave(E.id.transportable_capability, SIEffect.EMISSION)
    def on_transport_leave_emit(self, other):
        pass