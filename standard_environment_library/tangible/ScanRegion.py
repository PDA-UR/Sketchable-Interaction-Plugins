from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible

class ScanRegion(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ScanRegion __"
    region_display_name = "ScanRegion"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ScanRegion, self).__init__(shape, uuid, "", ScanRegion.regiontype, ScanRegion.regionname, kwargs)
        self.source = "libStdSI"
        self.color = PySI.Color(178, 235, 242, 128)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass
