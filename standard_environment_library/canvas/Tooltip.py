from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable


class Tooltip(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Tooltip __"
    region_display_name = "Tooltip"
    MOUSE_BUTTON_LEFT = 0
    MOUSE_BUTTON_RIGHT = 1
    MOUSE_BUTTON_MIDDLE = 2
    FILE_COPY = 3
    FILE_MOVE = 4
    MOUSE_MOVE = 5

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", Tooltip.regiontype, Tooltip.regionname, kwargs)
        self.qml_path = self.set_QML_path("Tooltip.qml")
        self.color = PySI.Color(255, 255, 255, 255)

        self.with_border = True


        self.textures = {
            Tooltip.MOUSE_BUTTON_LEFT: "res/mouse-left-button.png",
            Tooltip.MOUSE_BUTTON_RIGHT: "res/right-click-of-the-mouse.png",
            Tooltip.MOUSE_BUTTON_MIDDLE: "res/middle-mouse-click.png",
            Tooltip.FILE_COPY: "res/copy.png",
            Tooltip.FILE_MOVE: "res/move.png",
            Tooltip.MOUSE_MOVE: "res/mouse_move.png"
        }


        self.set_QML_data("img", "res/mouse-left-button.png", PySI.DataType.STRING)
        self.set_QML_data("height", self.height, PySI.DataType.FLOAT)
        self.set_QML_data("width", self.width, PySI.DataType.FLOAT)

    def update(self, text, texture_id):
        self.set_QML_data("img", self.textures[texture_id], PySI.DataType.STRING)
        self.set_QML_data("text", text, PySI.DataType.STRING)
        pass

