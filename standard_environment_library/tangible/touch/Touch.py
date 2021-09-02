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
        if self.press == self.HOVER:
            pass

        if self.press == self.DRAG:
            self.color = PySI.Color(255, 0, 0, 255)

        if self.press == self.TOUCH:
            pass

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        self.is_touching = False
        self.is_drawing = False
        self.is_dragging = False

        if self.press == self.HOVER:
            pass

        if self.press == self.TOUCH:
            self.is_touching = True

            if PySI.CollisionCapability.CLICK not in self.cap_emit.keys():
                self.enable_effect(PySI.CollisionCapability.CLICK, True, self.on_btn_press_enter_emit, self.on_btn_press_continuous_emit, self.on_btn_press_leave_emit)

        if self.press == self.DRAG:
            if self.is_new:
                self.enable_effect(PySI.CollisionCapability.SKETCH, True, self.on_sketch_enter_emit, self.on_sketch_continuous_emit, self.on_sketch_leave_emit)
                self.enable_effect(PySI.CollisionCapability.MOVE, True, self.on_move_enter_emit, self.on_move_continuous_emit, self.on_move_leave_emit)

                self.is_new = False
                return

            if len(self.present_collisions()) == 1 and self.present_collisions()[0] == canvas_uuid:
                if self.assigned_effect == "":
                    for k, v in self.selected_effects_by_cursor_id().items():
                        if k == self._uuid:
                            self.assigned_effect = v

                if self.assigned_effect != "":
                    self.color = PySI.Color(0, 0, 255, 255)
                    self.is_drawing = True
                    self.disable_effect(PySI.CollisionCapability.MOVE, True)
                else:
                    self.disable_effect(PySI.CollisionCapability.SKETCH, True)
            else:
                self.color = PySI.Color(255, 0, 0, 255)
                self.is_dragging = True
                self.disable_effect(PySI.CollisionCapability.SKETCH, True)

    @SIEffect.on_leave("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_leave_recv(self, canvas_uuid: str) -> None:
        if self.is_dragging:
            if PySI.CollisionCapability.MOVE in self.cap_emit.keys():
                self.disable_effect(PySI.CollisionCapability.MOVE, True)

                if self.move_target is not None:
                    self.move_target.on_move_leave_recv(*self.on_move_leave_emit(self.move_target))

        if self.is_drawing:
            self.disable_effect(PySI.CollisionCapability.SKETCH, True)

            if self.parent_canvas is not None:
                self.parent_canvas.on_sketch_leave_recv(*self.on_sketch_leave_emit(self.parent_canvas))
            self.parent_canvas = None

        if self.is_touching:
            if PySI.CollisionCapability.CLICK in self.cap_emit.keys():
                self.disable_effect(PySI.CollisionCapability.CLICK, True)
                if self.btn_target is not None:
                    self.btn_target.on_click_leave_recv(self._uuid)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_continuous(PySI.CollisionCapability.ASSIGN, SIEffect.RECEPTION)
    def on_assign_continuous_recv(self, effect_to_assign, effect_display_name, kwargs):
        if self.press == self.TOUCH:
            if self.assigned_effect != effect_to_assign:
                self.assigned_effect = effect_to_assign
                self.assign_effect(self.assigned_effect, effect_display_name, kwargs)

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

    def on_move_enter_emit(self, other):
        if self.move_target is None:
            self.move_target = other

        if self.move_target is other:
            return self._uuid, PySI.LinkingCapability.POSITION

        return "", ""

    def on_move_continuous_emit(self, other):
        self.emit_linking_action(self._uuid, PySI.LinkingCapability.POSITION, self.position())

    def on_move_leave_emit(self, other):
        if self.move_target is other:
            self.move_target = None
            return self._uuid, PySI.LinkingCapability.POSITION

        return "", ""

    def on_btn_press_enter_emit(self, other):
        if self.btn_target is None:
            self.btn_target = other

        return self._uuid

    def on_btn_press_continuous_emit(self, other):
        return self._uuid

    def on_btn_press_leave_emit(self, other):
        if self.btn_target is other:
            self.btn_target = None

        return self._uuid

    @SIEffect.on_continuous("ASSIGN", SIEffect.RECEPTION)
    def on_document_color_tool_assign_continuous_recv(self, tool_color):
        if self.is_touching:
            self.is_tool = True
            self.tool_color = tool_color

    @SIEffect.on_continuous("PARENT_DOCUMENT", SIEffect.RECEPTION)
    def on_document_parent_document_continuous_recv(self):
        if not self.is_tool:
            for r in self.current_regions():
                if r.name == Color.regionname:
                    if r.assigned_cursor == self._uuid:
                        self.is_tool = True
                        self.tool_color = r.color

        if self.is_tool:
            w, h = self.width, self.height
            x, y = self.absolute_x_pos(), self.absolute_y_pos()

            self.upper_rects_line.append([x, y])
            self.lower_rects_line.append([x, y + h])

            for r in self.current_regions():
                if r.regionname == Stroke.regionname:
                    if hasattr(r, "__is_in_drawing__") and hasattr(r, "__tool_source__"):
                        if r.__is_in_drawing__ and r.__tool_source__ == self._uuid:
                            s = self.upper_rects_line + self.lower_rects_line[::-1]

                            r.shape = PySI.PointVector(s)
                            return

            shape = [[x, y], [x, y + h], [x + w, y + h], [x + w, y]]
            self.create_region_via_name(shape, Stroke.regionname, kwargs={"tool": self._uuid, "is_in_drawing": True, "color": self.tool_color})

    @SIEffect.on_leave("PARENT_DOCUMENT", SIEffect.RECEPTION)
    def on_document_parent_document_leave_recv(self):
        for r in self.current_regions():
            if r.regionname == Stroke.regionname:
                if hasattr(r, "__is_in_drawing__") and hasattr(r, "__tool_source__"):
                    if r.__is_in_drawing__ and r.__tool_source__ == self._uuid:
                        r.__is_in_drawing__ = False

        self.upper_rects_line = []
        self.lower_rects_line = []
