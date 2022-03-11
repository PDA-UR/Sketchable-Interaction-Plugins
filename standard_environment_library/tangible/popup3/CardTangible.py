from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.E import E


class CardTangible(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ CardTangible __"
    region_display_name = "CardTangible"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", CardTangible.regiontype, CardTangible.regionname, kwargs)
        self.qml_path = ""
        self.color = PySI.Color(0, 0, 0, 0)
        self.evaluate_enveloped = True

    @SIEffect.on_continuous("__ SCAN __", SIEffect.RECEPTION)
    def on_tangible_scan_conitnuous_recv(self, is_active):
        if is_active:
            self.__notify__(f"", PySI.DataType.STRING)

    @SIEffect.on_leave("__ SCAN __", SIEffect.RECEPTION)
    def on_tangible_scan_leave_recv(self):
        pass

    def __update__(self, data: dict) -> None:
        if data["alive"]:
            super().__update__(data)
            self.shape = data["contour"]
        else:
            pass