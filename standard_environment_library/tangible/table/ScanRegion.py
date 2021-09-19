from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible

from plugins.E import E


class ScanRegion(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.scan_region_regionname
    region_display_name = E.id.scan_region_region_display_name

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ScanRegion, self).__init__(shape, uuid, "", ScanRegion.regiontype, ScanRegion.regionname, kwargs)

        self.with_border = True
        self.border_color = PySI.Color(255, 255, 255, 255)
        self.border_width = 8

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

        # if len(self.current_regions()) > 500:
        #     for r in self.current_regions():
        #         if r._uuid != self._uuid:
        #             r.delete()
        #
        #     import StartSIGRun
        #     StartSIGRun.start_application()
        #     self.delete()
        #     self.create_region_via_name(self.shape, ScanRegion.regionname, False, self.kwargs)

    # def __update__(self, data):
    #     self.shape = data["contour"]
    #     self.with_border = True
    #     self.border_color = PySI.Color(255, 255, 255, 255)