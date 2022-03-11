from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.automation.ConveyorBeltSpeedSlider import ConveyorBeltSpeedSlider
from plugins.E import E
import math
import time


class ConveyorBelt(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ ConveyorBelt __"
    region_display_name = "ConveyorBelt"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ConveyorBelt, self).__init__(shape, uuid, "res/factory.png", ConveyorBelt.regiontype, ConveyorBelt.regionname, kwargs)

        self.qml_path = self.set_QML_path("ConveyorBelt.qml")
        self.color = E.color.cb_color

        self.conveyor_point_step = 1
        self.conveyor_width = E.id.cb_width

        self.length = 0
        self.speed = 250  # px/s
        self.last_speed = 0

        self.delta_x = 0
        self.delta_y = 0

        self.collision_pixel_variance = 7
        self.transportation_path_changed = False

        # will contain tuples of (item_x, item_y, overall length up to this point, distance_x_to_prev_point, distance_y_to_prev_point
        self.transportation_path = []
        self.orig_shape = [p for p in self.shape]
        self.rebuild_shape()
        self.conveyed_items = {}
        self.drawing_additions = []
        self.slider_and_handle = None

        self.compute_drawing_additions()

    def compute_drawing_additions(self):
        self.drawing_additions = []
        x = 10
        prev_i = 0

        middle_line = [[e[0] - self.x, e[1] - self.y] for e in self.transportation_path]
        direction_visualization = []

        for i in range(len(middle_line)):
            if i != 0 and i % x == 0:
                direction_visualization.append(middle_line[prev_i:i][5:])
                prev_i = i

        for line in direction_visualization:
            self.drawing_additions.append([])
            arrow_part1, arrow_part2 = self.get_arrow_tip(line[-2], line[-1], 25, 2)
            self.drawing_additions[-1].append(list(arrow_part1))
            self.drawing_additions[-1].append(list(arrow_part2))
            self.drawing_additions[-1].append([list(line[0]), list(line[-1])])

        self.set_drawing_additions(self.drawing_additions)

    def get_arrow_tip(self, p: list, q: list, angle: float, part_stretch_factor: float) -> tuple:
        return self.get_arrow_tip_part(p, q, angle, part_stretch_factor), self.get_arrow_tip_part(p, q, 360 - angle, part_stretch_factor)

    def get_arrow_tip_part(self, p: list, q: list, angle: float, part_stretch_factor: float) -> list:
        pr = self.rotate(q, p, angle)
        qr = (p[0] - pr[0],  p[1] - pr[1])

        qr = [qr[0] * -part_stretch_factor + p[0], qr[1] * -part_stretch_factor + p[1]]

        return [qr, q]

    # def resample_points(self, points, num_desired_points=64):
    #     I = self.path_length(points) / (num_desired_points - 1)
    #     D = 0.0
    #
    #     new_points = [points[0]]
    #
    #     i = 1
    #
    #     while i < len(points):
    #         d = self.vector_norm((points[i - 1][0] - points[i][0], points[i - 1][1] - points[i][1]))
    #
    #         if (D + d) >= I:
    #             qx = points[i - 1][0] + ((I - D) / d) * (points[i][0] - points[i - 1][0])
    #             qy = points[i - 1][1] + ((I - D) / d) * (points[i][1] - points[i - 1][1])
    #             new_points.append((qx, qy))
    #             points.insert(i, (qx, qy))
    #
    #             D = 0.0
    #         else:
    #             D += d
    #
    #         i += 1
    #
    #     if len(new_points) == num_desired_points - 1:
    #         new_points.append(points[-1])
    #
    #     return new_points

    # def path_length(self, points):
    #     d = 0.0
    #
    #     for i in range(1, len(points)):
    #         d += self.vector_norm((points[i - 1][0] - points[i][0], points[i - 1][1] - points[i][1]))
    #
    #     return d

    def rotate(self, p: list, q: list, angle: float):
        ox, oy = p[0], p[1]
        px, py = q[0], q[1]

        qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
        qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)

        return qx, qy

    # def normalize_vector(self, v):
    #     n = float(self.vector_norm(v))
    #
    #     if n != 0:
    #         return [float(v[i]) / n for i in range(len(v))]
    #     else:
    #         return [-1 for i in range(len(v))]

    # def vector_norm(self, v):
    #     return math.sqrt(self.dot(v, v))

    # def dot(self, u, v):
    #     return sum((a * b) for a, b in zip(u, v))

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        x, y = self.relative_x_pos(), self.relative_y_pos() + self.height + 20
        slider_shape = [[x, y], [x, y + 30], [x + 300, y + 30], [x + 300, y]]

        self.create_region_via_name(slider_shape, ConveyorBeltSpeedSlider.regionname, False, {"parent": self._uuid})

    def build_transportation_path(self):
        self.transportation_path = []

        line = [(p.x + self.x, p.y + self.y) for p in self.orig_shape]

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

        self.compute_drawing_additions()

    def compute_conveyor_belt_item_insertion_position(self, other):
        target_segment_start_point_index = -1
        smallest_distance = 99999
        q = other.x + other.width / 2 + other.aabb[0].x, other.y + other.height / 2 + other.aabb[0].y  # use middle points of other

        for i, p in enumerate(self.transportation_path):
            r = q[0] - p[0], q[1] - p[1]

            distance = self.vector_length(r)

            if distance < smallest_distance:
                smallest_distance = distance
                target_segment_start_point_index = i

        return target_segment_start_point_index

    @SIEffect.on_enter(E.capability.transportable_transportable, SIEffect.EMISSION)
    def on_transport_enter_emit(self, item):
        segment_start_index = self.compute_conveyor_belt_item_insertion_position(item)
        segment_start_index = 1 if segment_start_index == 0 else segment_start_index
        distance = 0
        specific_path = []

        if self.transportation_path[segment_start_index] != (item.x, item.y):
            for i in range(segment_start_index, len(self.transportation_path)):
                distance += self.vector_length((self.transportation_path[i][0] - self.transportation_path[i - 1][0], self.transportation_path[i][1] - self.transportation_path[i - 1][1]))
                specific_path.append((self.transportation_path[i][0], self.transportation_path[i][1], distance))

            self.conveyed_items[item._uuid] = distance

        if not item.is_under_user_control:
            return self.transportation_path[segment_start_index][0], self.transportation_path[segment_start_index][1], distance, specific_path

        return item.x, item.y, distance, specific_path

    @SIEffect.on_continuous(E.capability.transportable_transportable, SIEffect.EMISSION)
    def on_transport_continuous_emit(self, item):
        if self.speed != self.last_speed:
            if (self.speed < 0 and self.last_speed > 0) or (self.speed > 0 and self.last_speed < 0):
                self.orig_shape.reverse()
                self.build_transportation_path()
                self.compute_drawing_additions()

            for r in self.current_regions():
                if (r._uuid == item._uuid) or (r._uuid not in self.conveyed_items.keys()):
                    continue

                r.on_transport_enter_recv(*self.on_transport_enter_emit(r))

            item.on_transport_enter_recv(*self.on_transport_enter_emit(item))

            self.last_speed = self.speed

        t = time.time() - item.transportation_starttime

        if self.transportation_path_changed:
            self.transportation_path_changed = False

            for i in range(len(item.transportation_path)):
                item.transportation_path[i] = item.transportation_path[i][0] + self.delta_x, item.transportation_path[i][1] + self.delta_y, item.transportation_path[i][2]

        if item.is_under_user_control or self.transportation_path is None:
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

            return item.x, item.y, False, False

        distance = (t * abs(self.speed)) % item.overall_transportation_length

        for i in range(1, len(item.transportation_path)):
            if i < len(item.transportation_path) - 1:
                if distance < item.transportation_path[i][2]:
                    p_from = item.transportation_path[i - 1]
                    p_to = item.transportation_path[i]
                    f = (distance - p_from[2]) / (p_to[2] - p_from[2])

                    x = p_from[0] + (p_to[0] - p_from[0]) * f
                    y = p_from[1] + (p_to[1] - p_from[1]) * f

                    closest_to_end = min(self.conveyed_items.items(), key=lambda x: x[1])

                    remaining_distance = 0
                    for k in range(i + 1, len(item.transportation_path)):
                        q = item.transportation_path[k]
                        p = item.transportation_path[i]
                        remaining_distance += self.vector_length((q[0] - p[0], q[1] - p[1]))
                    self.conveyed_items[item._uuid] = remaining_distance

                    return x, y, False, closest_to_end[0] == item._uuid

        return item.transportation_path[-1][0], item.transportation_path[-1][1], True, False

    @SIEffect.on_leave(E.capability.transportable_transportable, SIEffect.EMISSION)
    def on_transport_leave_emit(self, other):
        if other._uuid in self.conveyed_items:
            del self.conveyed_items[other._uuid]

    @SIEffect.on_link(SIEffect.RECEPTION, "push_speed", "push_speed")
    def speed_output_recv(self, speed: float, t: str, r: str) -> None:
        self.speed = speed
        self.slider_and_handle = t, r

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        Deletable.on_deletion_enter_recv(self)

        self.delete(self.slider_and_handle[0])
        self.delete(self.slider_and_handle[1])

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_continuous_recv(self):
        Deletable.on_deletion_continuous_recv(self)

        self.delete(self.slider_and_handle[0])
        self.delete(self.slider_and_handle[1])
