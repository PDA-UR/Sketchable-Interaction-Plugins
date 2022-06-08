from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable
from plugins.E import E


class Movable(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__MOVEABLE__"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super().__init__(shape, uuid, r, t, s, kwargs)
        self.move_border_color = PySI.Color(0, 255, 0, 255)
        self.default_border_color = PySI.Color(72, 79, 81, 255)

    @SIEffect.on_enter(PySI.CollisionCapability.MOVE, SIEffect.RECEPTION)
    def on_move_enter_recv(self, cursor_id, link_attrib):
        if cursor_id != "" and link_attrib != "":
            self.create_link(cursor_id, link_attrib, self._uuid, link_attrib)
            self.is_under_user_control = True
            self.was_under_user_control = False
            self.border_color = self.move_border_color

    @SIEffect.on_continuous(PySI.CollisionCapability.MOVE, SIEffect.RECEPTION)
    def on_move_continuous_recv(self):
        pass

    @SIEffect.on_leave(PySI.CollisionCapability.MOVE, SIEffect.RECEPTION)
    def on_move_leave_recv(self, cursor_id, link_attrib):
        if not cursor_id == "" and not link_attrib == "":
            lr = PySI.LinkRelation(cursor_id, link_attrib, self._uuid, link_attrib)

            if lr in self.link_relations:
                del self.link_relations[self.link_relations.index(lr)]

            self.is_under_user_control = False
            self.was_under_user_control = True
            self.border_color = self.default_border_color
