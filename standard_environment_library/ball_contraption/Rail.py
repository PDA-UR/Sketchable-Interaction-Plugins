from libPySI import PySI
from plugins.standard_environment_library.ball_contraption.physics_mixins.PhysicalSimulatable import PhysicalSimulatable


class Rail(PhysicalSimulatable):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Rail __"
    region_display_name = "Rail"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Rail, self).__init__(shape, uuid, "res/block.png", Rail.regiontype, Rail.regionname, self.configure_body_kwargs(kwargs))
        self.color = PySI.Color(0, 0, 255, 255)
        self.qml_path = self.set_QML_path("Rail.qml")

    def configure_body_kwargs(self, kwargs):
        kwargs["body"] = {
            "type": {
                PhysicalSimulatable.STATIC_BODY: {
                }
            },
            "shape": {
                "type": {
                    PhysicalSimulatable.POLYGON_SHAPE: {
                    }
                }
            }
        }
        return kwargs
