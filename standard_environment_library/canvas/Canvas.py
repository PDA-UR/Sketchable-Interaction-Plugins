from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class Canvas(SIEffect):
    regiontype = PySI.EffectType.SI_CANVAS
    regionname = PySI.EffectName.SI_STD_NAME_CANVAS

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Canvas, self).__init__(shape, uuid, "", Canvas.regiontype, Canvas.regionname, kwargs)
        self.color = PySI.Color(247, 249, 239, 255)
        self.log_file = open(".TEST.TXT", "r+")

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