from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class MagnetChoice(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ MagnetChoice __"
    region_display_name = "MagnetChoice"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", MagnetChoice.regiontype, MagnetChoice.regionname, kwargs)
        self.with_border = True
        self.border_width = 1
        self.parent = None if "parent" not in kwargs else kwargs["parent"]
        self.parent.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.color = kwargs["color"]
        self.recognized_shape = kwargs["recognized_shape"]

        if kwargs["recognized_shape"] == "":
            self.with_border = True
        else:
            self.with_border = False

        self.parent.choices.append(self)

    @SIEffect.on_enter("__MAGNET_CHOICE_DONE__", SIEffect.EMISSION)
    def on_magnet_choice_done_enter_emit(self, other) -> None:
        return self.color, self.recognized_shape

    @SIEffect.on_leave("__MAGNET_CHOICE_DONE__", SIEffect.EMISSION)
    def on_magnet_choice_done_leave_emit(self, other) -> None:
        return self.color, self.recognized_shape