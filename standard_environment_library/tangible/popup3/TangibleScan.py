from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class TangibleScan(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ TangibleScan __"
    region_display_name = "TangibleScan"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/scanner.png", TangibleScan.regiontype, TangibleScan.regionname, kwargs)
        self.qml_path = self.set_QML_path("TangibleScan.qml")
        self.color = PySI.Color(0, 80, 80, 255)
        self.to_ignore = []

    @SIEffect.on_continuous("__ SCAN __", SIEffect.EMISSION)
    def on_tangible_scan_continuous_emit(self, other):
        if other.enveloped_by(self) and other._uuid not in self.to_ignore:
            self.to_ignore.append(other._uuid)
            return True

        return False

    @SIEffect.on_leave("__ SCAN __", SIEffect.EMISSION)
    def on_tangible_scan_leave_emit(self, other):
        if other._uuid in self.to_ignore:
            self.to_ignore.remove(other._uuid)