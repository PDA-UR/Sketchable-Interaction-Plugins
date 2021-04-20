from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable


class Deletion(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_DELETION
    regionname = PySI.EffectName.SI_STD_NAME_DELETION
    region_display_name = "Deletion"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Deletion, self).__init__(shape, uuid, "res/deletion.png", Deletion.regiontype, Deletion.regionname, kwargs)

        self.qml_path = self.set_QML_path("Deletion.qml")
        self.color = PySI.Color(255, 255, 204, 255)
        self.is_under_user_control = False

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.EMISSION)
    def on_deletion_enter_emit(self, other):
        if other.regiontype is int(PySI.EffectType.SI_DELETION):
            if self.is_under_user_control:
                other.delete()

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.EMISSION)
    def on_deletion_continuous_emit(self, other):
        if other.regiontype is not int(PySI.EffectType.SI_DELETION):
            if not other.is_under_user_control:
                other.delete()
