from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

class OpenEntry(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = PySI.EffectName.SI_STD_NAME_OPEN_ENTRY
    region_display_name = "Open Folder/File"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(OpenEntry, self).__init__(shape, uuid, "res/open_entry.png", OpenEntry.regiontype, OpenEntry.regionname, kwargs)

        self.qml_path = self.set_QML_path("OpenEntry.qml")
        self.color = PySI.Color(204, 229, 255, 255)

    @SIEffect.on_enter(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.EMISSION)
    def on_open_entry_enter_emit(self, other):
        return self.is_under_user_control

    @SIEffect.on_continuous(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.EMISSION)
    def on_open_entry_continuous_emit(self, other):
        return self.is_under_user_control

    @SIEffect.on_leave(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.EMISSION)
    def on_open_entry_leave_emit(self, other):
        return self.is_under_user_control