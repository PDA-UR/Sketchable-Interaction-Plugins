from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E

from plugins.standard_environment_library.__UndoStack import UndoStack


class Canvas(SIEffect):
    regiontype = PySI.EffectType.SI_CANVAS
    regionname = PySI.EffectName.SI_STD_NAME_CANVAS

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Canvas, self).__init__(shape, uuid, "", Canvas.regiontype, Canvas.regionname, kwargs)

        self.color = PySI.Color(*kwargs["rgba"]) if "rgba" in kwargs else PySI.Color(247, 249, 239, 255)

        self.log_file = open(".TEST.TXT", "r+")
        self.ustack = UndoStack()
        self.can_undo = False

    @SIEffect.on_enter(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_enter_recv(self, x, y, sender_id):
        return 0

    @SIEffect.on_continuous(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_continuous_recv(self, x, y, cursor_id):
        self.add_point_to_region_drawing(x, y, cursor_id)

    @SIEffect.on_leave(PySI.CollisionCapability.SKETCH, SIEffect.RECEPTION)
    def on_sketch_leave_recv(self, x, y, cursor_id):
        self.register_region_from_drawing(cursor_id)

    @SIEffect.on_enter(E.id.canvas_logging_capability, SIEffect.EMISSION)
    def on_logging_enter_emit(self, other):
        pass

    @SIEffect.on_continuous(E.id.canvas_logging_capability, SIEffect.EMISSION)
    def on_logging_continuous_emit(self, other):
        message = self.log_file.read()

        if message != "":
            return message, True
        else:
            return "", False

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.EMISSION)
    def on_canvas_enter_emit(self, other):
        return self._uuid

    @SIEffect.on_link(SIEffect.RECEPTION, "__undo_stack_addition__", "__undo_stack_addition__")
    def on_add_unredoable_deletion_recv(self, target=None):
        if target != None:
            self.ustack.add(target)

    @SIEffect.on_link(SIEffect.RECEPTION, "__undo__", "__undo__")
    def on_canvas_undo_action_recv(self, t=None):
        o, q, ret = self.ustack.undo().get()

        if ret:
            self.__create_region__(o, q)

    @SIEffect.on_link(SIEffect.RECEPTION, "__redo__", "__redo__")
    def on_canvas_redo_action_recv(self, t=None):
        o, q, ret = self.ustack.redo().get()

        if ret:
            self.delete(o._uuid)
