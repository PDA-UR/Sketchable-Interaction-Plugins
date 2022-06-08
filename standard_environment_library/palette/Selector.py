from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class Selector(PositionLinkable, SIEffect):
    regionname = PySI.EffectName.SI_STD_NAME_SELECTOR
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Selector, self).__init__(shape, uuid, "", Selector.regiontype, Selector.regionname, kwargs)

        self.qml_path = self.set_QML_path("Selector.qml")

        self.color = kwargs["target_color"]
        self.target_name = kwargs["target_name"]
        self.target_display_name = kwargs["target_display_name"]
        self.target_texture_path = kwargs["target_texture"]
        self.name = "Selector for " + self.target_display_name
        self.default_border_color = PySI.Color(72, 79, 81, 255)
        self.with_border = True
        self.border_width = 3
        self.highlight_color = PySI.Color(0, 120, 215, 255)

        self.parent = kwargs["parent"]
        self.parent.selectors.append(self)

        self.middle_pt = kwargs["middle"]
        self.perp_vector = kwargs["perp_vector"]

        self.img_width = 40
        self.img_height = 40
        
        x, y = self.middle_pt
        pvx, pvy = self.perp_vector
        pt = x + pvx * self.img_width, y + pvy * self.img_height

        self.set_QML_data("img_path", self.target_texture_path, PySI.DataType.STRING)
        self.set_QML_data("visible", False, PySI.DataType.BOOL)
        self.set_QML_data("text", "", PySI.DataType.STRING)
        self.set_QML_data("img_width", self.img_width, PySI.DataType.INT)
        self.set_QML_data("img_height", self.img_height, PySI.DataType.INT)
        self.set_QML_data("text", self.target_display_name, PySI.DataType.STRING)
        self.set_QML_data("width", self.width, PySI.DataType.INT)
        self.set_QML_data("height", self.height, PySI.DataType.INT)
        self.set_QML_data("x", pt[0] - self.aabb[0].x - self.img_width / 2, PySI.DataType.FLOAT)
        self.set_QML_data("y", pt[1] - self.aabb[0].y - self.img_height / 2, PySI.DataType.FLOAT)

    @SIEffect.on_continuous(PySI.CollisionCapability.ASSIGN, SIEffect.EMISSION)
    def on_assign_continuous_emit(self, other):
        return self.target_name, self.target_display_name, self.target_texture_path, {}

    @SIEffect.on_enter(PySI.CollisionCapability.HOVER, SIEffect.RECEPTION)
    def on_hover_enter_recv(self):
        self.border_color = self.highlight_color

    @SIEffect.on_leave(PySI.CollisionCapability.HOVER, SIEffect.RECEPTION)
    def on_hover_leave_recv(self):
        self.border_color = self.default_border_color
