from libPySI import PySI
from plugins.standard_environment_library.ball_contraption.physics_mixins.PhysicalSimulatable import PhysicalSimulatable
from plugins.standard_environment_library.SIEffect import SIEffect


class Ball(PhysicalSimulatable):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Ball __"
    region_display_name = "Ball"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", r="", t="", s="", kwargs: dict = {}) -> None:
        super(Ball, self).__init__(shape, uuid, "res/sphere.png", Ball.regiontype, Ball.regionname, self.configure_body_kwargs(kwargs))
        self.qml_path = self.set_QML_path("Ball.qml")
        self.color = PySI.Color(255, 0, 0, 255)

    @SIEffect.on_enter("__PLAY_SOUND__", SIEffect.EMISSION)
    def on_play_sound_enter_emit(self, other):
        pass

    def configure_body_kwargs(self, kwargs):
        kwargs["body"] = {
            "type": {
                PhysicalSimulatable.DYNAMIC_BODY: {
                    "density": 1.0,
                    "friction": 0.01
                }
            },
            "shape": {
                "type": {
                    PhysicalSimulatable.CIRCLE_SHAPE: {
                        "radius": 50
                    }
                }
            }
        }

        return kwargs