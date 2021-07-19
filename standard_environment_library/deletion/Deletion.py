from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable


class Deletion(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_DELETION
    regionname = PySI.EffectName.SI_STD_NAME_DELETION
    region_display_name = "Deletion"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Deletion, self).__init__(shape, uuid, "res/deletion.png", Deletion.regiontype, Deletion.regionname, kwargs)

        self.qml_path = self.set_QML_path("Deletion.qml")
        self.color = PySI.Color(255, 255, 204, 255)
        self.is_under_user_control = False
        self.last_deletion = None

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.EMISSION)
    def on_deletion_enter_emit(self, other):
        if other.regiontype == int(PySI.EffectType.SI_DELETION):
            if self.is_under_user_control:
                self.last_deletion = other
                self.emit_linking_action(self._uuid, "__undo_stack_addition__", self.on_add_unredoable_deletion_emit)
                other.delete()

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.EMISSION)
    def on_deletion_continuous_emit(self, other):
        if other.regiontype != int(PySI.EffectType.SI_DELETION):
            if not other.is_under_user_control:
                self.last_deletion = other
                self.emit_linking_action(self._uuid, "__undo_stack_addition__", self.on_add_unredoable_deletion_emit)
                other.delete()

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, parent_uuid):
        self.create_link(self._uuid, "__undo_stack_addition__", parent_uuid, "__undo_stack_addition__")

    @SIEffect.on_link(SIEffect.EMISSION, "__undo_stack_addition__")
    def on_add_unredoable_deletion_emit(self):
        return self.last_deletion