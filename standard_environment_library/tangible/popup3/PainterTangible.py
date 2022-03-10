from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library.paint_test.Painter import Painter
from plugins.E import E
import math


class PainterTangible(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ PainterTangible __"
    region_display_name = "PainterTangible"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, SIEffect.TEXTURE_PATH_NONE, PainterTangible.regiontype, PainterTangible.regionname, kwargs)
        self.color = kwargs["color"]
        self.stroke_width = 10
        self.to_radians = math.pi / 180
        self.prev_x = kwargs["x"]
        self.prev_y = kwargs["y"]
        self.initial_x = kwargs["x"]
        self.initial_y = kwargs["y"]
        self.parent_canvas = None

        s = []
        w = self.stroke_width
        cx, cy = kwargs["x"], kwargs["y"]

        for i in range(360):
            x, y = w / 2 * math.cos(i * self.to_radians) + cx, w / 2 * math.sin(i * self.to_radians) + cy
            s.append([x, y])

        self.shape = PySI.PointVector(s)

    def __update__(self, data: dict) -> None:
        if data["alive"]:
            super().__update__(data)
            self.color = data["color"]
            self.move(self.x + (data["x"] - self.prev_x), self.y + (data["y"] - self.prev_y))
            self.prev_x = data["x"]
            self.prev_y = data["y"]
        else:
            if self.parent_canvas is not None:
                self.parent_canvas.on_sketch_leave_recv(*self.on_sketch_leave_emit(self.parent_canvas))
                self.delete()

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        self.assign_effect(Painter.regionname, Painter.region_display_name, "", {})

    @SIEffect.on_enter(PySI.CollisionCapability.SKETCH, SIEffect.EMISSION)
    def on_sketch_enter_emit(self, other):
        self.parent_canvas = other
        self.set_cursor_stroke_width_by_cursorid(self._uuid, self.stroke_width)
        self.set_cursor_stroke_color_by_cursorid(self._uuid, self.color)
        return self.x + self.initial_x, self.y + self.initial_y, self._uuid

    @SIEffect.on_continuous(PySI.CollisionCapability.SKETCH, SIEffect.EMISSION)
    def on_sketch_continuous_emit(self, other):
        return self.x + self.initial_x, self.y + self.initial_y, self._uuid

    @SIEffect.on_cleave(PySI.CollisionCapability.SKETCH, SIEffect.EMISSION)
    def on_sketch_leave_emit(self, other):
        self.parent_canvas = None

        kwargs = {}
        kwargs["color"] = self.color
        kwargs["stroke_width"] = self.stroke_width
        kwargs["resampling"] = False

        return self.x + self.initial_x, self.y + self.initial_y, self._uuid, False, kwargs


