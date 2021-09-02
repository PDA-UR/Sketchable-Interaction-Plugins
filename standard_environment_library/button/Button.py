from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable

from plugins.E import E

class Button(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_BUTTON
    regionname = PySI.EffectName.SI_STD_NAME_BUTTON
    region_width = E.id.button_width
    region_height = E.id.button_height

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        if kwargs["value"]:
            super(Button, self).__init__(shape, uuid, E.id.button_rev_texture, Button.regiontype, Button.regionname, kwargs)
        else:
            super(Button, self).__init__(shape, uuid, E.id.button_fwd_texture, Button.regiontype, Button.regionname, kwargs)

        self.with_border = False

        self.qml_path = self.set_QML_path(E.id.button_qml_path)
        self.color = E.color.button_color

        self.value = kwargs["value"] if len(kwargs.keys()) else False
        self.parent = str(kwargs["parent"]) if len(kwargs.keys()) else ""

        self.is_triggered = False
        self.is_triggered_reported = False

        self.icon_width = 100
        self.icon_height = 100
        self.width = Button.region_width
        self.height = Button.region_height

        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)

        self.parent = ""
        self.is_open_entry_capability_blocked = False

    @SIEffect.on_enter(PySI.CollisionCapability.BTN, SIEffect.EMISSION)
    def on_btn_enter_emit(self, other):
        return "", ""

    @SIEffect.on_continuous(PySI.CollisionCapability.BTN, SIEffect.EMISSION)
    def on_btn_continuous_emit(self, other):
        if self.is_triggered and not self.is_triggered_reported and other.is_open_entry_capability_blocked:
            self.is_triggered_reported = True
            return self._uuid, self.value

        return "", ""

    @SIEffect.on_leave(PySI.CollisionCapability.BTN, SIEffect.EMISSION)
    def on_btn_leave_emit(self, other):
        return "", ""

    @SIEffect.on_enter(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_enter_recv(self, cursor_id):
        self.is_triggered = False
        self.is_triggered_reported = False

    @SIEffect.on_continuous(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_continuous_recv(self, cursor_id):
        self.is_triggered = True

    @SIEffect.on_leave(PySI.CollisionCapability.CLICK, SIEffect.RECEPTION)
    def on_click_leave_recv(self, cursor_id):
        self.is_triggered = False

    @SIEffect.on_enter(PySI.CollisionCapability.PARENT, SIEffect.RECEPTION)
    def on_parent_enter_recv(self, parent_id):
        if self.parent == "":
            self.parent = parent_id
            self.create_link(parent_id, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_leave(PySI.CollisionCapability.PARENT, SIEffect.RECEPTION)
    def on_parent_leave_recv(self, parent_id):
        if self.parent == parent_id:
            self.remove_link(parent_id, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
