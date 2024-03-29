from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

from plugins.E import E

class Undo(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.undo_regionname
    region_display_name = E.id.undo_region_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Undo, self).__init__(shape, uuid, E.id.undo_texture, Undo.regiontype, Undo.regionname, kwargs)
        self.qml_path = self.set_QML_path(E.id.undo_qml_path)

    @SIEffect.on_enter(E.capability.undo_undo, SIEffect.EMISSION)
    def __on_undo_enter_emit__(self, other):
        pass

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, parent_uuid):
        self.create_link(self._uuid, E.capability.undo_undo, parent_uuid, E.capability.undo_undo)

    @SIEffect.on_link(SIEffect.EMISSION, E.capability.undo_undo)
    def on_canvas_undo_action_emit(self):
        pass

    @SIEffect.on_enter(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_enter_recv(self, cursor_id):
         self.emit_linking_action(self._uuid, E.capability.undo_undo, self.on_canvas_undo_action_emit)

    @SIEffect.on_leave(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_leave_recv(self, cursor_id):
        pass