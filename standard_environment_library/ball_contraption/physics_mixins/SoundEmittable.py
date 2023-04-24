from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
import playsound


class SoundEmittable(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ SoundEmittable __"
    region_display_name = "SoundEmittable"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", r="", t="", s="", kwargs: dict = {}) -> None:
        super(SoundEmittable, self).__init__(shape, uuid, r, t, s, kwargs)
        self.sound_player_function = playsound.playsound
        self.path_to_sound = kwargs["sound"]

    @SIEffect.on_enter("__PLAY_SOUND__", SIEffect.RECEPTION)
    def on_play_sound_enter_recv(self):
        playsound.playsound(self.path_to_sound, block=False)