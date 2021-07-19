from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

class Redo(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Redo __"
    region_display_name = "Redo"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Redo, self).__init__(shape, uuid, "res/redo.png", Redo.regiontype, Redo.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = self.set_QML_path("Redo.qml")

    @SIEffect.on_enter("redo", SIEffect.EMISSION)
    def __on_redo_enter_emit__(self, other):
        pass

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, parent_uuid):
        self.create_link(self._uuid, "__redo__", parent_uuid, "__redo__")

    @SIEffect.on_link(SIEffect.EMISSION, "__redo__")
    def on_canvas_redo_action_emit(self):
        pass

    @SIEffect.on_enter(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_enter_recv(self, cursor_id):
        self.emit_linking_action(self._uuid, "__redo__", self.on_canvas_redo_action_emit)

    @SIEffect.on_leave(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_leave_recv(self, cursor_id):
        pass