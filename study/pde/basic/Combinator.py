from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class Combinator(PositionLinkable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Combinator Region __"
    region_display_name = "Combinator"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", Combinator.regiontype, Combinator.regionname, kwargs)
        self.color = PySI.Color(255, 0, 0, 0)
        self.with_border = True
        self.parent = None if "parent" not in kwargs else kwargs["parent"]
        self.parent.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.parent.combinator = self

        self.color_filter = []
        self.shape_filter = []

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_enter("__MAGNET_CHOICE_DONE__", SIEffect.RECEPTION)
    def on_magnet_choice_done_enter_recv(self, color, recognized_shape) -> None:
        if recognized_shape == "":
            self.color_filter.append([color.r, color.g, color.b])
        else:
            self.shape_filter.append(recognized_shape)

    @SIEffect.on_leave("__MAGNET_CHOICE_DONE__", SIEffect.RECEPTION)
    def on_magnet_choice_done_leave_recv(self, color, recognized_shape) -> None:
        if recognized_shape == "":
            del self.color_filter[self.color_filter.index([color.r, color.g, color.b])]
        else:
            del self.shape_filter[self.shape_filter.index(recognized_shape)]
