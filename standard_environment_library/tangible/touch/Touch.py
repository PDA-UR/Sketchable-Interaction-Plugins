from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Tangible import Tangible
from plugins.standard_environment_library.tangible.document.draw.Stroke import Stroke
from plugins.standard_environment_library.tangible.document.tools.Color import Color

from plugins.E import E


class Touch(Tangible):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Touch __"
    region_display_name = "Touch"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "", Touch.regiontype, Touch.regionname, kwargs)

        self.color = PySI.Color(0, 0, 0, 0)
        self.with_border = False
        self.HOVER = -1
        self.TOUCH = 0
        self.DRAG = 1

        self.press = kwargs["press"]
        self.finger = kwargs["finger"]
        self.assigned_effect = ""
        self.tool_color = None

        self.parent_canvas = None
        self.move_target = None
        self.btn_target = None

        self.last_x = 0
        self.last_y = 0

        self.is_drawing = False
        self.is_dragging = False
        self.is_touching = False

        self.is_tool = False
        self.drawing_shape = []
        self._uuid = str(self.s_id)
        self.first_point = True
        self.is_new = True

        self.upper_rects_line = []
        self.lower_rects_line = []


    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        if PySI.CollisionCapability.SKETCH not in self.cap_recv:
            self.enable_effect(PySI.CollisionCapability.SKETCH, True, self.on_sketch_enter_emit, self.on_sketch_continuous_emit, self.on_sketch_leave_emit)
            self.assigned_effect = Stroke.regionname
            self.assign_effect(self.assigned_effect, Stroke.region_display_name, {})

    @SIEffect.on_leave("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_leave_recv(self, canvas_uuid: str) -> None:
        if self.parent_canvas is not None:
            self.parent_canvas.on_sketch_leave_recv(*self.on_sketch_leave_emit(self.parent_canvas))

            self.parent_canvas = None

        if PySI.CollisionCapability.SKETCH not in self.cap_recv:
            self.disable_effect(PySI.CollisionCapability.SKETCH, True)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_continuous(PySI.CollisionCapability.ASSIGN, SIEffect.RECEPTION)
    def on_assign_continuous_recv(self, effect_to_assign, effect_display_name, kwargs):
        return

    def on_sketch_enter_emit(self, other):
        self.parent_canvas = other

        return 0, 0, self._uuid

    def on_sketch_continuous_emit(self, other):
        if self.first_point:
            self.first_point = False

            return self.aabb[0].x + self.x, self.aabb[0].y + self.y, self._uuid, False

        return self.aabb[0].x + self.x, self.aabb[0].y + self.y, self._uuid

    def on_sketch_leave_emit(self, other):
        self.parent_canvas = None

        return 0, 0, self._uuid