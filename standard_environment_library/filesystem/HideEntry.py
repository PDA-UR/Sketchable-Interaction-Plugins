from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class HideEntry(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ HideEntry __"
    region_display_name = "HideEntry"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/hide.png", HideEntry.regiontype, HideEntry.regionname, kwargs)
        self.qml_path = self.set_QML_path("HideEntry.qml")
        self.color = PySI.Color(205, 205, 154, 255)

    @SIEffect.on_enter("__HIDE_ENTRY_", SIEffect.EMISSION)
    def on_hide_entry_enter_emit(self, other):
        pass

    @SIEffect.on_enter("__HIDE_ENTRY_", SIEffect.RECEPTION)
    def on_hide_entry_enter_recv(self):
        self.delete()