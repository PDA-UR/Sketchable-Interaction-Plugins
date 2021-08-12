from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible

class ScanRegion(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ScanRegion__"
    region_display_name = "ScanRegion"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ScanRegion, self).__init__(shape, uuid, "", ScanRegion.regiontype, ScanRegion.regionname, kwargs)
        self.color = PySI.Color(5, 5, 5, 100)
        self.source = "libStdSI"
        self.kwargs = kwargs

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        if len(self.current_regions()) > 500:
            for r in self.current_regions():
                if r._uuid != self._uuid:
                    r.delete()

            import StartSIGRun
            StartSIGRun.start_application()
            self.delete()
            self.create_region_via_name(self.shape, ScanRegion.regionname, False, self.kwargs)
