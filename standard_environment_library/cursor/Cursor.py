from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect

from plugins.E import E
import re


class Cursor(SIEffect):
    regiontype = PySI.EffectType.SI_MOUSE_CURSOR
    regionname = PySI.EffectName.SI_STD_NAME_MOUSE_CURSOR
    region_width = E.id.cursor_width
    region_height = E.id.cursor_height

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", Cursor.regiontype, Cursor.regionname, kwargs)

        self.kwargs = kwargs

        self.qml_path = self.set_QML_path(E.id.cursor_qml_path)
        # self.color = PySI.Color(255, 0, 0, 255)
        self.color = E.color.cursor_color

        self.assigned_effect = ""
        self.is_drawing_blocked = False
        self.width = Cursor.region_width
        self.height = Cursor.region_height

        self.visualization_width = 500
        self.visualization_height = 500

        self.with_border = False

        self.clicks = 0

        self.parent_canvas = None
        self.move_target = None
        self.btn_target = None
        self.image_editor_tool = []
        self.image_editor_tooltype = None

        self.left_mouse_active = False
        self.right_mouse_active = False
        self.middle_mouse_active = False

        self.current_effect_texture = ""
        self.current_effect_name = ""
        self.set_QML_data("movement_texture", "res/movement.png", PySI.DataType.STRING)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        return self.x - self.last_x, self.y - self.last_y, self.x, self.y

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        if len(self.present_collisions_names()) == 1 and self.present_collisions_names()[0] == PySI.EffectName.SI_STD_NAME_CANVAS:
            self.set_QML_data("visible", True, PySI.DataType.BOOL)
        else:
            testRegex = re.compile(r'__SI_CANVAS_NAME__|__SI_PALETTE_NAME__|Selector for (A-Za-z0-9)*')

            is_valid = True
            for t in self.present_collisions_names():
                is_valid &= testRegex.search(t) is not None

            if not is_valid:
                self.set_QML_data("visible", False, PySI.DataType.BOOL)

        self.last_x = self.x
        self.last_y = self.y

        self.move(abs_x, abs_y)

    def on_sketch_enter_emit(self, other):
        self.parent_canvas = other

        return 0, 0, self._uuid

    def on_sketch_continuous_emit(self, other):
        return self.x, self.y, self._uuid

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
        pass

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

    def on_middle_mouse_click(self, is_active):
        self.middle_mouse_active = is_active

        if is_active:
            if E.capability.cursor_enlarge not in self.cap_emit.keys():
                self.enable_effect(E.capability.cursor_enlarge, True, self.on_enlarge_enter_emit, None, None)
        else:
            if E.capability.cursor_enlarge in self.cap_emit.keys():
                self.disable_effect(E.capability.cursor_enlarge, True)

    def on_enlarge_enter_emit(self, other):
        pass

    def on_left_mouse_click(self, is_active):
        self.left_mouse_active = is_active

        if self.kwargs["draw"] == "RMB":
            self.handle_move(is_active)
        elif self.kwargs["draw"] == "LMB":
            self.handle_drawing_click(is_active)

    def handle_drawing_click(self, is_active):
        if is_active:
            if PySI.CollisionCapability.CLICK not in self.cap_emit.keys():
                self.enable_effect(PySI.CollisionCapability.CLICK, True, self.on_btn_press_enter_emit, self.on_btn_press_continuous_emit, self.on_btn_press_leave_emit)

            if self.assigned_effect != "":
                if not self.is_drawing_blocked and PySI.CollisionCapability.SKETCH not in self.cap_emit.keys():
                    self.enable_effect(PySI.CollisionCapability.SKETCH, True, self.on_sketch_enter_emit, self.on_sketch_continuous_emit, self.on_sketch_leave_emit)
        else:
            if PySI.CollisionCapability.SKETCH in self.cap_emit.keys():
                self.disable_effect(PySI.CollisionCapability.SKETCH, True)

                if self.parent_canvas is not None:
                    self.parent_canvas.on_sketch_leave_recv(*self.on_sketch_leave_emit(self.parent_canvas))
                self.parent_canvas = None

            if PySI.CollisionCapability.CLICK in self.cap_emit.keys():
                self.disable_effect(PySI.CollisionCapability.CLICK, True)
                if self.btn_target is not None:
                    self.btn_target.on_click_leave_recv(self._uuid)

    def on_right_mouse_click(self, is_active):
        self.right_mouse_active = is_active

        if self.kwargs["draw"] == "RMB":
            self.handle_drawing_click(is_active)
        elif self.kwargs["draw"] == "LMB":
            self.handle_move(is_active)

    def handle_move(self, is_active):
        if is_active:
            if PySI.CollisionCapability.MOVE not in self.cap_emit.keys():
                self.enable_effect(PySI.CollisionCapability.MOVE, True, self.on_move_enter_emit, self.on_move_continuous_emit, self.on_move_leave_emit)
        elif PySI.CollisionCapability.MOVE in self.cap_emit.keys():
            self.disable_effect(PySI.CollisionCapability.MOVE, True)
            if self.move_target is not None:
                self.move_target.on_move_leave_recv(*self.on_move_leave_emit(self.move_target))

    @SIEffect.on_continuous(PySI.CollisionCapability.ASSIGN, SIEffect.RECEPTION)
    def on_assign_continuous_recv(self, effect_to_assign, effect_display_name, effect_texture, kwargs):
        if self.left_mouse_active:
            if self.assigned_effect != effect_to_assign:
                self.assigned_effect = effect_to_assign
                self.current_effect_texture = effect_texture
                self.current_effect_name = effect_display_name

                self.set_QML_data("effect_texture", effect_texture, PySI.DataType.STRING)
                self.set_QML_data("effect_text", effect_display_name, PySI.DataType.STRING)
                self.set_QML_data("visible", True, PySI.DataType.BOOL)



                self.assign_effect(self.assigned_effect, effect_display_name, effect_texture, kwargs)

    @SIEffect.on_continuous(E.capability.cursor_image_editor_assign, SIEffect.RECEPTION)
    def on_image_editor_assign_continuous_recv(self):
        pass

    @SIEffect.on_enter(PySI.CollisionCapability.HOVER, SIEffect.EMISSION)
    def on_hover_enter_emit(self, other):
        pass

    @SIEffect.on_leave(PySI.CollisionCapability.HOVER, SIEffect.EMISSION)
    def on_hover_leave_emit(self, other):
        pass

    @SIEffect.on_continuous(E.capability.cursor_image_editor_tool_activation, SIEffect.EMISSION)
    def on_tool_activation_continuous_emit(self, other):
        if self.left_mouse_active:
            # self.disable_effect(PySI.CollisionCapability.SKETCH, True)
            self.is_drawing_blocked = True
            return True
        else:
            self.is_drawing_blocked = False

        return False

    @SIEffect.on_leave(E.capability.cursor_image_editor_tool_hiding, SIEffect.RECEPTION)
    def on_hide_tool_leave_recv(self):
        for tool in self.image_editor_tool:
            tool.delete()