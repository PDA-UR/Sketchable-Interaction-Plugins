from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable

class CursorVisualization(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Cursor Visualization __"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "res/movement.png", CursorVisualization.regiontype, CursorVisualization.regionname, kwargs)

        self.arrow_cursor_texture_color = "res/mouse_cursor_red.png" if kwargs["id"] == 0 else "res/mouse_cursor_green.png" if kwargs["id"] == 1 else "res/mouse_cursor_blue.png" if kwargs["id"] == 2 else "res/mouse_cursor.png"
        self.move_cursor_texture_color = "res/movement_red.png" if kwargs["id"] == 0 else "res/movement_green.png" if kwargs["id"] == 1 else "res/movement_blue.png" if kwargs["id"] == 2 else "res/movement.png"

        self.color = PySI.Color(0, 0, 0, 0)
        self.with_border = False
        self.qml_path = self.set_QML_path("CursorVisualization.qml")

        self.set_QML_data("img_width", int(self.width), PySI.DataType.INT)
        self.set_QML_data("img_height", int(self.height), PySI.DataType.INT)
        self.set_QML_data("width", int(self.width), PySI.DataType.INT)
        self.set_QML_data("height", int(self.height), PySI.DataType.INT)
        self.set_QML_data("img_path", self.arrow_cursor_texture_color, PySI.DataType.STRING)

        self.parent = kwargs["parent"]
        self.width_factor = kwargs["width_factor"]
        self.id = kwargs["id"]
        self.parent.visualization = self

        self.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

        pass

    def trigger_move(self, toggle):
        if toggle:
            self.shape = PySI.PointVector([[self.aabb[0].x, self.y], [self.aabb[0].x, self.aabb[0].y + self.height], [self.aabb[0].x + self.height, self.aabb[0].y + self.height], [self.aabb[0].x + self.height, self.aabb[0].y]])
            self.set_QML_data("img_width", int(self.width), PySI.DataType.INT)
            self.set_QML_data("img_height", int(self.height), PySI.DataType.INT)
            self.set_QML_data("width", int(self.width), PySI.DataType.INT)
            self.set_QML_data("height", int(self.height), PySI.DataType.INT)
            self.set_QML_data("img_path", self.move_cursor_texture_color, PySI.DataType.STRING)
        else:
            self.shape = PySI.PointVector([[self.aabb[0].x, self.aabb[0].y], [self.aabb[0].x, self.aabb[0].y + self.height], [self.aabb[0].x + self.height * self.width_factor, self.aabb[0].y + self.height], [self.aabb[0].x + self.height * self.width_factor, self.aabb[0].y]])
            self.set_QML_data("img_path", self.arrow_cursor_texture_color, PySI.DataType.STRING)
            self.set_QML_data("img_width", int(self.width), PySI.DataType.INT)
            self.set_QML_data("img_height", int(self.height), PySI.DataType.INT)
            self.set_QML_data("width", int(self.width), PySI.DataType.INT)
            self.set_QML_data("height", int(self.height), PySI.DataType.INT)