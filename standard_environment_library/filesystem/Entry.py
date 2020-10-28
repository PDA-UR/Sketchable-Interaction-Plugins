from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Transportable import Transportable
from plugins.E import E


class Entry(Transportable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_ENTRY
    regionname = PySI.EffectName.SI_STD_NAME_ENTRY

    def __init__(self, shape=PySI.PointVector(), uuid="", regiontype=PySI.EffectType.SI_ENTRY, regionname=PySI.EffectName.SI_STD_NAME_ENTRY, kwargs={}):
        Transportable.__init__(self, shape, uuid, self.TEXTURE_PATH_NONE, regiontype, regionname, kwargs)
        Movable.__init__(self, shape, uuid, self.TEXTURE_PATH_NONE, regiontype, regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, self.TEXTURE_PATH_NONE, regiontype, regionname, kwargs)

        self.width = 130
        self.height = 125
        self.icon_width = 65
        self.icon_height = 75
        self.text_height = 50
        self.color = PySI.Color(255, 10, 0, 0)
        self.text_color = "#FF000000"
        self.path = str(kwargs["cwd"]) if len(kwargs.keys()) else ""
        self.parent = str(kwargs["parent"]) if len(kwargs.keys()) else ""
        self.filename = ""
        self.is_visible = True
        self.is_under_user_control = False
        self.is_open_entry_capability_blocked = False
        self.with_border = False

        if self.path != "":
            self.filename = self.path[self.path.rfind("/") + 1:]

        self.is_container_visible = True

        self.set_QML_data("text_height", self.text_height, PySI.DataType.INT)
        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
        self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
        self.set_QML_data("name", self.filename, PySI.DataType.STRING)

        if self.parent != "":
            self.create_link(self.parent, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_enter(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.RECEPTION)
    def on_open_entry_enter_recv(self, is_other_controlled):
        pass

    @SIEffect.on_continuous(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.RECEPTION)
    def on_open_entry_continuous_recv(self, is_other_controlled):
        if self.parent == "" and not self.is_open_entry_capability_blocked and not self.is_under_user_control and not is_other_controlled:
            self.start_standard_application(self._uuid, self.path)
            self.is_open_entry_capability_blocked = True

    @SIEffect.on_leave(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.RECEPTION)
    def on_open_entry_leave_recv(self, is_other_controlled):
        if self.parent == "" and self.is_open_entry_capability_blocked:
            self.close_standard_application(self._uuid)
            self.is_open_entry_capability_blocked = False

    @SIEffect.on_enter(PySI.CollisionCapability.PARENT, SIEffect.RECEPTION)
    def on_parent_enter_recv(self, _uuid):
        if _uuid != "":
            if self.parent == "":
                self.parent = _uuid
                self.create_link(_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_leave(PySI.CollisionCapability.PARENT, SIEffect.RECEPTION)
    def on_parent_leave_recv(self, _uuid):
        if _uuid != "":
            if self.parent == _uuid:
                self.parent = ""
                self.remove_link(_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)