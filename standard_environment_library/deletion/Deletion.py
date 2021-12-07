from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

from plugins.E import E


class Deletion(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_DELETION
    regionname = PySI.EffectName.SI_STD_NAME_DELETION
    region_display_name = E.id.deletion_region_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Deletion, self).__init__(shape, uuid, E.id.deletion_texture, Deletion.regiontype, Deletion.regionname, kwargs)

        self.qml_path = self.set_QML_path(E.id.deletion_qml_path)
        self.color = E.color.deletion_color
        self.is_under_user_control = False
        self.last_deletion = None

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.EMISSION)
    def on_deletion_enter_emit(self, other):
        if other.regiontype == int(PySI.EffectType.SI_DELETION):
            if other.__unredoable_deletion__:
                if self.is_under_user_control:
                    self.last_deletion = other
                    self.emit_linking_action(self._uuid, E.capability.deletion_undo_stack_addition, self.on_add_unredoable_deletion_emit)

            else:
                if self.is_under_user_control:
                    other.delete()

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.EMISSION)
    def on_deletion_continuous_emit(self, other):
        if other.regiontype != int(PySI.EffectType.SI_DELETION):
            if not other.is_under_user_control:
                if other.__unredoable_deletion__:
                    self.last_deletion = other
                    self.emit_linking_action(self._uuid, E.capability.deletion_undo_stack_addition, self.on_add_unredoable_deletion_emit)

                other.delete()
        else:
            other.delete()

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, parent_uuid):
        self.create_link(self._uuid, E.capability.deletion_undo_stack_addition, parent_uuid, E.capability.deletion_undo_stack_addition)

    @SIEffect.on_link(SIEffect.EMISSION, E.capability.deletion_undo_stack_addition)
    def on_add_unredoable_deletion_emit(self):
        return self.last_deletion