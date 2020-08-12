from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect

import numpy as np
import math
import time


class ConveyorBelt(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ ConveyorBelt __"
    region_display_name = "ConveyorBelt"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ConveyorBelt, self).__init__(shape, uuid, "res/factory.png", ConveyorBelt.regiontype, ConveyorBelt.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = self.set_QML_path("ConveyorBelt.qml")
        self.color = PySI.Color(120, 255, 120, 255)

        self.conveyor_point_step = 1
        self.conveyor_width = 75

        self.length = 0
        self.speed = 350

        self.transportation_path = []
        self.rebuild_shape()

        self.enable_effect("TRANSPORT", SIEffect.EMISSION, None, self.on_transport_continuous_emit, self.on_transport_leave_emit)

    def build_transportation_path(self):
        line = [(p.x, p.y) for p in self.shape]

        for i in range(1, len(line), self.conveyor_point_step):
            dx = line[i][0] - line[i - 1][0]
            dy = line[i][1] - line[i - 1][1]

            self.length += math.sqrt(dx * dx + dy * dy)
            self.transportation_path.append((line[i][0], line[i][1], self.length))

        self.transportation_path = self.transportation_path[2:-2]

    def build_shape(self):
        shape, shape_part_one, shape_part_two = [], [], []

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

    def transportation_start_condition(self, item_x, item_y):
        d = 100000
        idx = 0

        for i in range(len(self.transportation_path)):
            dp = item_x - self.transportation_path[i][0], item_y - self.transportation_path[i][1]
            dn = self.vector_length(dp)

            if dn < d:
                d = dn
                idx = i

        length = 0
        for i in range(1, idx):
            dp = self.transportation_path[i][0] - self.transportation_path[i - 1][0], self.transportation_path[i][1] - self.transportation_path[i - 1][1]
            length += self.vector_length(dp)

        return self.transportation_path[idx][0], self.transportation_path[idx][1], idx, time.time(), self._uuid, False, length

    def transportation_intermediate_condition(self, item):
        if item.transporter == self._uuid and not item.is_transport_done:
            if self.length > 0 and hasattr(item, "actual_transportation_length"):
                t = time.time() - item.transportation_starttime

                distance = (t * self.speed) % self.length + item.actual_transportation_length

                for i in range(1, len(self.transportation_path)):
                    if distance < self.transportation_path[i][2]:
                        if item.prev_point_idx - i > len(self.transportation_path) - 15:
                            if not item.is_transport_done:
                                return self.transportation_path[-1][0], self.transportation_path[-1][1], len(self.transportation_path) - 1, 0, self._uuid, True, 0
                        else:
                            item.cb_transportation_active = True

                            p_from = self.transportation_path[i - 1]
                            p_to = self.transportation_path[i]
                            f = (distance - p_from[2]) / (p_to[2] - p_from[2])

                            x = p_from[0] + (p_to[0] - p_from[0]) * f
                            y = p_from[1] + (p_to[1] - p_from[1]) * f

                            return x, y, i, 0, self._uuid, False, 0

                    if item.prev_point_idx >= len(self.transportation_path) - 3:
                        item.is_transport_done = True
                        break

        return None, None, None, None, None, None, None

    def transportation_current_condition(self, item):
        if not item.is_under_user_control and hasattr(item, "is_transport_done") and not item.is_transport_done:
            if not item.cb_transportation_active and item.transporter == "":
                return self.transportation_start_condition(item.x, item.y)

            return self.transportation_intermediate_condition(item)

        return None, None, None, None, None, None, None

    def on_transport_continuous_emit(self, other):
        return self.transportation_current_condition(other)

    def on_transport_leave_emit(self, other):
        if other.cb_transportation_active:
            # print("post transport")
            pass
        else:
            # print("no transport")
            pass

    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        super(ConveyorBelt, self).set_position_from_position(rel_x, rel_y, abs_x, abs_y)

        for i in range(len(self.transportation_path)):
            self.transportation_path[i] = self.transportation_path[i][0] + rel_x, self.transportation_path[i][1] + rel_y, self.transportation_path[i][2]
