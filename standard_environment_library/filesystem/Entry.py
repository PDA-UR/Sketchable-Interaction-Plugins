from libPySI import PySI

from plugins.standard_environment_library import SIEffect


class Entry(SIEffect.SIEffect):
    regiontype = PySI.EffectType.SI_ENTRY
    regionname = PySI.EffectName.SI_STD_NAME_ENTRY

    def __init__(self, shape=PySI.PointVector(), uuid="", regiontype=PySI.EffectType.SI_ENTRY, regionname=PySI.EffectName.SI_STD_NAME_ENTRY, kwargs={}):
        super(Entry, self).__init__(shape, uuid, self.TEXTURE_PATH_NONE, regiontype, regionname, kwargs)
        self.source = "libstdSI"
        self.qml_path = ""
        self.width = 130
        self.height = 125
        self.icon_width = 65
        self.icon_height = 75
        self.text_height = 50
        self.color = PySI.Color(255, 10, 0, 0)
        self.text_color = "#FFFFFFFF"
        self.path = str(kwargs["cwd"]) if len(kwargs.keys()) else ""
        self.parent = str(kwargs["parent"]) if len(kwargs.keys()) else ""
        self.filename = ""
        self.is_visible = True
        self.is_under_user_control = False
        self.is_open_entry_capability_blocked = False
        self.transportation_starttime = 0
        self.prev_point_idx = 0
        self.cb_transportation_active = False
        self.transporter = ""
        self.is_transport_done = False
        self.actual_transportation_length = 0

        self.disable_effect(PySI.CollisionCapability.DELETION, self.RECEPTION)
        self.enable_effect("TRANSPORT", self.RECEPTION, None, self.on_transport_continuous_recv, self.on_transport_leave_recv)

        if self.path is not "":
            self.filename = self.path[self.path.rfind("/") + 1:]

        self.is_container_visible = True

        self.set_QML_data("text_height", self.text_height, PySI.DataType.INT)
        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
        self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
        self.set_QML_data("name", self.filename, PySI.DataType.STRING)

        self.enable_effect(PySI.CollisionCapability.OPEN_ENTRY, self.RECEPTION, self.on_open_entry_enter_recv, self.on_open_entry_continuous_recv, self.on_open_entry_leave_recv)
        self.enable_effect(PySI.CollisionCapability.PARENT, self.RECEPTION, self.on_parent_enter_recv, None, self.on_parent_leave_recv)

        if self.parent != "":
            self.create_link(self.parent, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    def on_open_entry_enter_recv(self, is_other_controlled):
        pass

    def on_open_entry_continuous_recv(self, is_other_controlled):
        if self.parent == "" and not self.is_open_entry_capability_blocked and not self.is_under_user_control and not is_other_controlled:
            self.start_standard_application(self._uuid, self.path)
            self.is_open_entry_capability_blocked = True

    def on_open_entry_leave_recv(self, is_other_controlled):
        if self.parent == "" and self.is_open_entry_capability_blocked:
            self.close_standard_application(self._uuid)
            self.is_open_entry_capability_blocked = False

    def on_parent_enter_recv(self, _uuid):
        if _uuid != "":
            if self.parent == "":
                self.parent = _uuid
                self.create_link(_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    def on_parent_leave_recv(self, _uuid):
        if _uuid != "":
            if self.parent == _uuid:
                self.parent = ""
                self.remove_link(_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    def on_transport_continuous_recv(self, x, y, previous_point_index, t, transporter, is_transport_done, transportation_length):
        if not self.is_under_user_control:
            if x is not None and y is not None:
                self.is_transport_done = is_transport_done
                self.prev_point_idx = previous_point_index

                if not self.cb_transportation_active and self.transporter == "":
                    self.actual_transportation_length = transportation_length
                    self.transportation_starttime = t
                    self.cb_transportation_active = True
                    self.transporter = transporter

                self.move(x - self.relative_x_pos() - self.width / 2, y - self.relative_y_pos() - self.height / 2)

    def on_transport_leave_recv(self):
        self.transportation_starttime = 0
        self.cb_transportation_active = False
        self.transporter = ""
        self.prev_point_idx = 0
        self.is_transport_done = False
        self.actual_transportation_length = 0
