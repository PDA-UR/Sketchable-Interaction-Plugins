from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.ball_contraption.physics_mixins.SoundEmittable import SoundEmittable
from plugins.standard_environment_library.ball_contraption.physics_mixins.PhysicalSimulatable import PhysicalSimulatable
import os


class SoundRail_G(SoundEmittable, PhysicalSimulatable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ SoundRail G__"
    region_display_name = "SoundRail G"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        kwargs["sound"] = os.getcwd() + "/plugins/study/pde/res/xylophone-g.wav"
        super(SoundRail_G, self).__init__(shape, uuid, "res/xylophone-g.png", SoundRail_G.regiontype, SoundRail_G.regionname, self.configure_body_kwargs(kwargs))
        self.qml_path = self.set_QML_path("Bell.qml")
        self.color = PySI.Color(164, 116, 73, 255)

    @SIEffect.on_enter("__PLAY_SOUND__", SIEffect.RECEPTION)
    def on_play_sound_enter_recv(self):
        super().on_play_sound_enter_recv()
        regions = [r for r in self.current_regions() if r.regionname == "__ JingleObserver __"]

        if len(regions) == 1:
            regions[0].register_played_sound("G")

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