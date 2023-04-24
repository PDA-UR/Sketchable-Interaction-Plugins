from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from Box2D import Box2D
import math
import numpy as np
from scipy.spatial import ConvexHull


class PhysicalSimulatable(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ GravityAttractable __"
    region_display_name = "GravityAttractable"
    CIRCLE_SHAPE = 0
    POLYGON_SHAPE = 1
    STATIC_BODY = Box2D.b2_staticBody
    DYNAMIC_BODY = Box2D.b2_dynamicBody

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", r="", t="", s="", kwargs: dict = {}) -> None:
        super(PhysicalSimulatable, self).__init__(shape, uuid, r, t, s, kwargs)
        self.is_drawn = "__name__" in kwargs.keys()

        if not self.is_drawn:
            return

        body_type = list(kwargs["body"]["type"].keys())[0]
        self.shape_type = list(kwargs["body"]["shape"]["type"].keys())[0]
        self.body_def = Box2D.b2BodyDef()
        self.body_def.type = body_type
        self.parent_world = None
        self.body = None
        self.b2_shape = None
        self.fixture_def = Box2D.b2FixtureDef()

        if self.shape_type == self.CIRCLE_SHAPE:
            self.setup_circle_shape(kwargs)

        if self.shape_type == self.POLYGON_SHAPE:
            self.setup_polygon_shape(kwargs)

        self.width = self.get_region_width()
        self.height = self.get_region_height()
        self.cw, self.ch = self.context_dimensions()
        self.body_def.position.Set(self.aabb[0].x, self.ch - self.aabb[0].y)

        self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)

    def setup_circle_shape(self, kwargs):
        self.density = kwargs["body"]["type"][self.body_def.type]["density"] if self.body_def.type == self.DYNAMIC_BODY else 0
        self.friction = kwargs["body"]["type"][self.body_def.type]["friction"] if self.body_def.type == self.DYNAMIC_BODY else 0
        self.radius = kwargs["body"]["shape"]["type"][self.shape_type]["radius"]

        shape = [[(self.radius + 5) * math.cos(i * math.pi / 180) + self.aabb[0].x + (self.radius + 5) / 2, (self.radius + 5) * math.sin(i * math.pi / 180) + self.aabb[0].y + (self.radius + 5) / 2] for i in range(360)]

        self.shape = PySI.PointVector(shape)

    def setup_polygon_shape(self, kwargs):
        self.bounding_rect = [[p[0], p[1]] for p in self.minimum_bounding_rectangle([[p.x, p.y] for p in self.shape])]
        self.shape = PySI.PointVector([[p[0], p[1]] for p in self.bounding_rect])

    @SIEffect.on_enter("__PARENT_GRAVITY__", SIEffect.EMISSION)
    def on_gravity_enter_emit(self, gravity):
        if not self.is_drawn:
            return

        self.parent_world = gravity.physics_world
        self.body = self.parent_world.CreateBody(self.body_def)

        if self.shape_type == self.POLYGON_SHAPE:
            self.setup_polygon_body()

        if self.shape_type == self.CIRCLE_SHAPE:
            self.setup_circle_body()

        self.body.CreateFixture(self.fixture_def)
        self.body.userData = {"uuid": self._uuid}

        gravity.create_link(gravity._uuid, "__WORLD_UPDATE__", self._uuid, "POS")

    def setup_polygon_body(self):
        self.b2_shape = Box2D.b2PolygonShape()
        self.b2_shape.vertices = [[p[0] - self.aabb[0].x, -(p[1] - self.aabb[0].y)] for p in self.bounding_rect]
        self.b2_shape.vertexCount = len(self.bounding_rect)
        self.fixture_def.shape = self.b2_shape

    def setup_circle_body(self):
        self.b2_shape = Box2D.b2CircleShape(pos=(0, 0), radius=self.radius)
        self.fixture_def.shape = self.b2_shape
        self.fixture_def.density = self.density
        self.fixture_def.friction = self.friction

    @SIEffect.on_link(SIEffect.RECEPTION, "__WORLD_UPDATE__", "POS")
    def on_world_step(self, target, _):
        if target == self._uuid:
            if self.is_under_user_control:
                self.update_body_position()
            elif self.body_def.type == self.DYNAMIC_BODY:
                x, y = self.body.position.x, self.ch - self.body.position.y
                dx, dy = x - self.aabb[0].x - self.radius, y - self.aabb[0].y - self.radius

                self.move(dx, dy)
                self.set_QML_data("rotation", self.body.angle * 50, PySI.DataType.FLOAT)

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        super().on_deletion_enter_recv()
        if not self.is_under_user_control:
            self.parent_world.DestroyBody(self.body)

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_continuous_recv(self):
        super().on_deletion_continuous_recv()
        if not self.is_under_user_control:
            self.parent_world.DestroyBody(self.body)

    def update_body_position(self):
        x, y, = self.absolute_x_pos(), self.ch - self.absolute_y_pos()
        self.body.position = Box2D.b2Vec2(x, y)
        self.body.linearVelocity = Box2D.b2Vec2(0, 0)

    def configure_body_kwargs(self, kwargs):
        # override in target class
        return kwargs

    def minimum_bounding_rectangle(self, points):
        """
        Retrieved from: https://gis.stackexchange.com/questions/22895/finding-minimum-area-rectangle-for-given-points

        Find the smallest bounding rectangle for a set of points.
        Returns a set of points representing the corners of the bounding box.

        :param points: an nx2 matrix of coordinates
        :rval: an nx2 matrix of coordinates
        """
        points = np.array(points)
        from scipy.ndimage.interpolation import rotate
        pi2 = np.pi/2.

        # get the convex hull for the points
        hull_points = points[ConvexHull(points).vertices]

        # calculate edge angles
        edges = np.zeros((len(hull_points)-1, 2))
        edges = hull_points[1:] - hull_points[:-1]

        angles = np.zeros((len(edges)))
        angles = np.arctan2(edges[:, 1], edges[:, 0])

        angles = np.abs(np.mod(angles, pi2))
        angles = np.unique(angles)

        # find rotation matrices
        # XXX both work
        rotations = np.vstack([
            np.cos(angles),
            np.cos(angles-pi2),
            np.cos(angles+pi2),
            np.cos(angles)]).T

        rotations = rotations.reshape((-1, 2, 2))

        # apply rotations to the hull
        rot_points = np.dot(rotations, hull_points.T)

        # find the bounding points
        min_x = np.nanmin(rot_points[:, 0], axis=1)
        max_x = np.nanmax(rot_points[:, 0], axis=1)
        min_y = np.nanmin(rot_points[:, 1], axis=1)
        max_y = np.nanmax(rot_points[:, 1], axis=1)

        # find the box with the best area
        areas = (max_x - min_x) * (max_y - min_y)
        best_idx = np.argmin(areas)

        # return the best box
        x1 = max_x[best_idx]
        x2 = min_x[best_idx]
        y1 = max_y[best_idx]
        y2 = min_y[best_idx]
        r = rotations[best_idx]

        rval = np.zeros((4, 2))
        rval[0] = np.dot([x1, y2], r)
        rval[1] = np.dot([x2, y2], r)
        rval[2] = np.dot([x2, y1], r)
        rval[3] = np.dot([x1, y1], r)

        return rval
