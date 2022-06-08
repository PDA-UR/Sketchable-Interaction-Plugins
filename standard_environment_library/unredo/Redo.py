from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

from plugins.E import E

class Redo(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.redo_regionname
    region_display_name = E.id.redo_region_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Redo, self).__init__(shape, uuid, E.id.redo_texture, Redo.regiontype, Redo.regionname, kwargs)
        self.qml_path = self.set_QML_path(E.id.redo_qml_path)

    @SIEffect.on_enter(E.capability.redo_redo, SIEffect.EMISSION)
    def __on_redo_enter_emit__(self, other):
        pass

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, parent_uuid):
        self.create_link(self._uuid, E.capability.redo_redo, parent_uuid, E.capability.redo_redo)

    @SIEffect.on_link(SIEffect.EMISSION, E.capability.redo_redo)
    def on_canvas_redo_action_emit(self):
        pass

    @SIEffect.on_enter(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_enter_recv(self, cursor_id):
        self.emit_linking_action(self._uuid, E.capability.redo_redo, self.on_canvas_redo_action_emit)

    @SIEffect.on_leave(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_leave_recv(self, cursor_id):
        pass