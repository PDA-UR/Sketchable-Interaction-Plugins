from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class ColorPicker(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ ColorPicker __"
    region_display_name = "ColorPicker"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/colorpicker.png", ColorPicker.regiontype, ColorPicker.regionname, kwargs)
        cw, ch = self.context_dimensions()

        self.qml_path = self.set_QML_path("ColorPicker.qml")
        self.color = PySI.Color(180, 180, 180, 180)
        self.r = 0
        self.g = 0
        self.b = 0

        self.border_width = int(2 * cw / 1920)

        self.target_width = int(200 * cw / 1920)
        self.target_height = self.target_width

        self.shape = PySI.PointVector(self.round_edge([
            [self.aabb[0].x, self.aabb[0].y],
            [self.aabb[0].x, self.aabb[0].y + self.target_height],
            [self.aabb[0].x + self.target_width, self.aabb[0].y + self.target_height],
            [self.aabb[0].x + self.target_width, self.aabb[0].y]
        ]))

        # self.width = int(self.aabb[3].x - self.aabb[0].x)
        # self.height = int(self.aabb[1].y - self.aabb[0].y)

        self.set_QML_data("width", float(self.width), PySI.DataType.FLOAT)
        self.set_QML_data("height", float(self.height), PySI.DataType.FLOAT)

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        color_str = self.get_QML_data("color", PySI.DataType.STRING)
        if len(color_str) == 7:
            r, g, b = self.color_string_to_rgb(color_str)
            if r != self.r or g != self.g or self.b != b:
                self.r, self.g, self.b = r, g, b

    @SIEffect.on_continuous("__RECOLOR__", SIEffect.EMISSION)
    def on_recolor_continuous_emit(self, other):
        return self.r, self.g, self.b

    def color_string_to_rgb(self, col_str):
        col_str = col_str[1:]
        r_str = col_str[:2]
        g_str = col_str[2:4]
        b_str = col_str[4:]

        return int(r_str, 16), int(g_str, 16), int(b_str, 16)