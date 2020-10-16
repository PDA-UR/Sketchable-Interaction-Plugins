from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class Selector(PositionLinkable, SIEffect):
    regionname = PySI.EffectName.SI_STD_NAME_SELECTOR
    regiontype = PySI.EffectType.SI_SELECTOR

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        PositionLinkable.__init__(self, shape, uuid, "", Selector.regiontype, Selector.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, "", Selector.regiontype, Selector.regionname, kwargs)
        self.qml_path = self.set_QML_path("Selector.qml")

        self.color = kwargs["target_color"]
        self.target_name = kwargs["target_name"]
        self.target_display_name = kwargs["target_display_name"]
        self.target_texture_path = kwargs["target_texture"]
        self.name = "Selector for " + self.target_display_name

        self.parent = kwargs["parent"]

        self.img_width = 40
        self.img_height = 40

        self.set_QML_data("img_path", self.target_texture_path, PySI.DataType.STRING)
        self.set_QML_data("visible", False, PySI.DataType.BOOL)
        self.set_QML_data("text", "", PySI.DataType.STRING)
        self.set_QML_data("img_width", self.img_width, PySI.DataType.INT)
        self.set_QML_data("img_height", self.img_height, PySI.DataType.INT)
        self.set_QML_data("text", self.target_display_name, PySI.DataType.STRING)
        self.set_QML_data("width", self.width, PySI.DataType.INT)
        self.set_QML_data("height", self.height, PySI.DataType.INT)

        self.create_link(self.parent, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_continuous(PySI.CollisionCapability.ASSIGN, SIEffect.EMISSION)
    def on_assign_continuous_emit(self, other):
        return self.target_name, self.target_display_name, {}

    @SIEffect.on_enter(PySI.CollisionCapability.HOVER, SIEffect.RECEPTION)
    def on_hover_enter_recv(self):
        self.set_QML_data("visible", True, PySI.DataType.BOOL)

    @SIEffect.on_leave(PySI.CollisionCapability.HOVER, SIEffect.RECEPTION)
    def on_hover_leave_recv(self):
        self.set_QML_data("visible", False, PySI.DataType.BOOL)
