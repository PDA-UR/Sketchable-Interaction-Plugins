from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible


class Flasher(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Flasher __"
    region_display_name = "Flasher"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Flasher, self).__init__(shape, uuid, "", Flasher.regiontype, Flasher.regionname, kwargs)
        self.color = PySI.Color(0, 0, 0, 0)

    @SIEffect.on_enter("__PARENT_FLASH__", SIEffect.EMISSION)
    def on_flash_enter_emit(self, other: object) -> None:
        pass

    @SIEffect.on_leave("__PARENT_FLASH__", SIEffect.EMISSION)
    def on_flash_leave_emit(self, other: object) -> None:
        pass