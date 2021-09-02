from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E

from plugins.standard_environment_library.__UndoStack import UndoStack


class Canvas(SIEffect):
    regiontype = PySI.EffectType.SI_CANVAS
    regionname = PySI.EffectName.SI_STD_NAME_CANVAS

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", Canvas.regiontype, Canvas.regionname, kwargs)

        self.color = PySI.Color(*kwargs["rgba"]) if "rgba" in kwargs else E.color.canvas_color

        self.log_file = open(".TEST.TXT", "r+")
        self.ustack = UndoStack()
        self.can_undo = False

    @SIEffect.on_enter(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_enter_recv(self, x, y, sender_id):
        return 0

    @SIEffect.on_continuous(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_continuous_recv(self, x, y, cursor_id, add=True):
        if add:
            self.add_point_to_region_drawing(x, y, cursor_id)

    @SIEffect.on_leave(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_leave_recv(self, x, y, cursor_id):
        self.register_region_from_drawing(cursor_id)

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
