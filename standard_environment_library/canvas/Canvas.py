from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E

from plugins.standard_environment_library.__UndoStack import UndoStack
from plugins.standard_environment_library.canvas.FPS_Counter import FPS_Counter
from plugins.standard_environment_library.canvas.Tooltip import Tooltip


class Canvas(SIEffect):
    regiontype = PySI.EffectType.SI_CANVAS
    regionname = PySI.EffectName.SI_STD_NAME_CANVAS
    resampling_enabled = True

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", Canvas.regiontype, Canvas.regionname, kwargs)

        w, h = self.context_dimensions()

        self.color = PySI.Color(*kwargs["rgba"]) if "rgba" in kwargs else E.color.canvas_color
        self.old_color = self.color
        self.with_border = False
        self.log_file = open(".TEST.TXT", "r+")
        self.ustack = UndoStack()
        self.can_undo = False

        self.create_region_via_name(PySI.PointVector([[w - 110, 10], [w - 110, 35], [w - 10, 35], [w - 10, 10]]), FPS_Counter.regionname, kwargs=kwargs)

    @SIEffect.on_enter(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_enter_recv(self, x, y, cursor_id):
        if x == 0 and y == 0:
            return

        self.add_point_to_region_drawing(x, y, cursor_id)

    @SIEffect.on_continuous(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_continuous_recv(self, x, y, cursor_id, add=True):
        if add:
            self.add_point_to_region_drawing(x, y, cursor_id)

    @SIEffect.on_leave(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_leave_recv(self, x, y, cursor_id, is_canceled, kwargs):
        if "ignore" in kwargs and kwargs["ignore"]:
            return

        self.add_point_to_region_drawing(x, y, cursor_id)
        if not is_canceled:
            self.register_region_from_drawing(cursor_id, kwargs)
        else:
            self.cancel_region_drawing(cursor_id)

    @SIEffect.on_enter(E.capability.canvas_logging, SIEffect.EMISSION)
    def on_logging_enter_emit(self, other):
        pass

    @SIEffect.on_continuous(E.capability.canvas_logging, SIEffect.EMISSION)
    def on_logging_continuous_emit(self, other):
        message = self.log_file.read()

        if message != "":
            return message, True
        else:
            return "", False

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.EMISSION)
    def on_canvas_enter_emit(self, other):
        return self._uuid

    @SIEffect.on_continuous(E.capability.canvas_parent, SIEffect.EMISSION)
    def on_canvas_continuous_emit(self, other):
        return self._uuid

    # @SIEffect.on_continuous("__PARENT_GRAVITY__", SIEffect.EMISSION)
    # def on_gravity_continuous_emit(self, other):
    #     return self._uuid

    @SIEffect.on_leave(E.capability.canvas_parent, SIEffect.EMISSION)
    def on_canvas_leave_emit(self, other):
        return self._uuid

    @SIEffect.on_link(SIEffect.RECEPTION, E.capability.deletion_undo_stack_addition, E.capability.deletion_undo_stack_addition)
    def on_add_unredoable_deletion_recv(self, target=None):
        if target != None:
            self.ustack.add(target)

    @SIEffect.on_link(SIEffect.RECEPTION, E.capability.undo_undo, E.capability.undo_undo)
    def on_canvas_undo_action_recv(self, t=None):
        o, q, ret = self.ustack.undo().get()

        if ret:
            self.__create_region__(o, q)

    @SIEffect.on_link(SIEffect.RECEPTION, E.capability.redo_redo, E.capability.redo_redo)
    def on_canvas_redo_action_recv(self, t=None):
        o, q, ret = self.ustack.redo().get()

        if ret:
            self.delete(o._uuid)

    @SIEffect.on_enter("__PARENT_FLASH__", SIEffect.RECEPTION)
    def on_flash_enter_recv(self) -> None:
        self.old_color = PySI.Color(self.color.r, self.color.g, self.color.b, self.color.a)
        self.color = PySI.Color(255, 255, 255, 255)

    @SIEffect.on_leave("__PARENT_FLASH__", SIEffect.RECEPTION)
    def on_flash_leave_recv(self) -> None:
        self.color = PySI.Color(self.old_color.r, self.old_color.g, self.old_color.b, self.old_color.a)
