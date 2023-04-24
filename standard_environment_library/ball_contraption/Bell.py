from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.ball_contraption.physics_mixins.SoundEmittable import SoundEmittable
import os


class Bell(SoundEmittable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Bell __"
    region_display_name = "Bell"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        kwargs["sound"] = os.getcwd() + "/plugins/study/pde/res/bell.mp3"
        super(Bell, self).__init__(shape, uuid, "res/bell.png", Bell.regiontype, Bell.regionname, kwargs)
        self.qml_path = self.set_QML_path("Bell.qml")
        self.color = PySI.Color(226, 126, 7, 255)