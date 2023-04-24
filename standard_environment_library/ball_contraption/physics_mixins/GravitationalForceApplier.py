from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from Box2D import Box2D
from datetime import datetime


class GravitationalForceApplier(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ GravitationalForceApplier __"
    region_display_name = "GravitationalForceApplier"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", r="", t="", s="", kwargs: dict = {}) -> None:
        super(GravitationalForceApplier, self).__init__(shape, uuid, r, t, s, kwargs)
        self.color = PySI.Color(0, 0, 0, 0)
        self.gravity = Box2D.b2Vec2(*kwargs["gravity"])
        self.physics_world = Box2D.b2World(self.gravity)
        self.physics_world.contactListener = Box2D.b2ContactListener()
        self.velocity_iterations = 6
        self.position_iterations = 2
        self.with_border = False
        self.cw, self.ch = self.context_dimensions()
        self.time = datetime.now()

        # self.ground_body_def = Box2D.b2BodyDef()
        # self.ground_body_def.type = Box2D.b2_staticBody
        # self.ground_body_def.position.Set(self.cw / 2, 5.0)
        # self.ground_body = self.physics_world.CreateBody(self.ground_body_def)
        #
        # self.ground_box = Box2D.b2PolygonShape()
        # self.ground_box.SetAsBox(self.cw / 2, 2.5)
        # self.fixture_def = Box2D.b2FixtureDef()
        # self.fixture_def.shape = self.ground_box
        #
        # self.ground_body.CreateFixture(self.fixture_def)

    @SIEffect.on_continuous(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid):
        t = datetime.now()
        deltatime = (t - self.time).total_seconds()
        self.time = t

        self.physics_world.Step(deltatime, self.velocity_iterations, self.position_iterations)

        for b in self.physics_world.bodies:
            if b.userData is not None:
                self.target = str(b.userData["uuid"])
                self.emit_linking_action(self._uuid, "__WORLD_UPDATE__", self.on_world_step())

    @SIEffect.on_enter("__PARENT_GRAVITY__", SIEffect.RECEPTION)
    def on_gravity_enter_recv(self):
        pass

    @SIEffect.on_link(SIEffect.EMISSION, "__WORLD_UPDATE__")
    def on_world_step(self):
        return self.target, None