from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library.filesystem.File import File
from datetime import datetime
from plugins.E import E


class InboxItem(File):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ InboxItem __"
    region_display_name = "InboxItem"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(InboxItem, self).__init__(shape, uuid, "res/email.png", InboxItem.regiontype, InboxItem.regionname, kwargs)
        cw, ch = self.context_dimensions()
        self.default_border_color = PySI.Color(72, 79, 81, 255)
        self.color = self.default_border_color
        self.border_color = self.default_border_color
        self.qml_path = self.set_QML_path("InboxItem.qml")
        self.default_height = self.height
        self.default_width = self.width
        self.parent = kwargs["parent"]
        self.is_email: SIEffect.SI_CONDITION = True

        self.email_sender = kwargs["data"]["email_sender"]
        self.email_receiver = kwargs["data"]["email_receiver"]
        self.email_subject = kwargs["data"]["email_subject"]
        self.email_message = kwargs["data"]["message"]

        if hasattr(self.parent, "inbox_items"):
            self.parent.inbox_items.append(self)
            self.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

        self.with_border = True
        self.border_width = int(2 * cw / 1920)
        self.date = datetime.now()
        self.datetime = self.date.strftime("%d.%m.%Y, %H:%M:%S Uhr") if "date" not in kwargs["data"] else kwargs["data"]["date"]
        self.can_enter = False
        self.icon_width = 65 * cw / 1920
        self.icon_height = 75 * ch / 1080
        self.is_unread = kwargs["data"]["is_unread"]

        self.read_width = cw / 5
        self.read_height = int(self.read_width * 29.7 / 21)

        self.is_in_item_view = True
        self.is_in_icon_view = False
        self.is_in_read_view = False

        self.entryname = "Mail:" + self.email_subject

        self.set_QML_data("email_subject", self.email_subject, PySI.DataType.STRING)
        self.set_QML_data("email_sender", self.email_sender, PySI.DataType.STRING)
        self.set_QML_data("email_receiver", self.email_receiver, PySI.DataType.STRING)
        self.set_QML_data("email_message", self.email_message, PySI.DataType.STRING)
        self.set_QML_data("item_view", self.is_in_item_view, PySI.DataType.BOOL)
        self.set_QML_data("icon_view", self.is_in_icon_view, PySI.DataType.BOOL)
        self.set_QML_data("read_view", self.is_in_read_view, PySI.DataType.BOOL)
        self.set_QML_data("is_unread", self.is_unread, PySI.DataType.BOOL)
        self.set_QML_data("date", self.datetime, PySI.DataType.STRING)

        if not hasattr(self.parent, "inbox_items"):
            self.to_icon_view()

    @SIEffect.on_enter("__INBOX_ENTRY__", SIEffect.RECEPTION)
    def on_inbox_entry_enter_recv(self):
        pass

    def to_item_view(self, inbox):
        self.parent = inbox

        self.color = self.default_border_color
        self.width = self.default_width
        self.height = self.default_height

        self.shape = PySI.PointVector([[self.aabb[0].x, self.aabb[0].y],
                                       [self.aabb[0].x, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y]])

        self.is_in_icon_view = False
        self.is_in_read_view = False
        self.is_in_item_view = True

        self.set_QML_data("item_view", self.is_in_item_view, PySI.DataType.BOOL)
        self.set_QML_data("icon_view", self.is_in_icon_view, PySI.DataType.BOOL)
        self.set_QML_data("read_view", self.is_in_read_view, PySI.DataType.BOOL)
        self.set_QML_data("widget_width", self.width, PySI.DataType.INT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.INT)

    @SIEffect.on_continuous("__INBOX_ENTRY__", SIEffect.RECEPTION)
    def on_inbox_entry_continuous_recv(self, change_view, inbox):
        if change_view:
            self.to_item_view(inbox)

    def to_icon_view(self):
        self.is_ready = True
        self.parent = None
        self.with_border = False
        self.color = PySI.Color(0, 0, 0, 0)
        self.width = int(self.icon_width)
        self.height = int(self.icon_height + 50)
        self.shape = PySI.PointVector([[self.aabb[0].x, self.aabb[0].y],
                                       [self.aabb[0].x, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y]
                                       ])
        self.is_in_icon_view = True
        self.is_in_read_view = False
        self.is_in_item_view = False

        self.set_QML_data("item_view", self.is_in_item_view, PySI.DataType.BOOL)
        self.set_QML_data("icon_view", self.is_in_icon_view, PySI.DataType.BOOL)
        self.set_QML_data("read_view", self.is_in_read_view, PySI.DataType.BOOL)
        self.set_QML_data("widget_width", self.width, PySI.DataType.INT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.INT)
        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)

    @SIEffect.on_leave("__INBOX_ENTRY__", SIEffect.RECEPTION)
    def on_inbox_entry_leave_recv(self):
        self.can_enter = True
        self.to_icon_view()
        self.snap_to_mouse()

    def to_read_view(self):
        self.with_border = True
        self.is_unread = False
        self.color = PySI.Color(230, 230, 230, 255)
        self.width = self.read_width
        self.height = self.read_height
        self.shape = PySI.PointVector([[self.aabb[0].x, self.aabb[0].y],
                                       [self.aabb[0].x, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y]
                                       ])

        self.is_in_icon_view = False
        self.is_in_read_view = True
        self.is_in_item_view = False

        self.set_QML_data("item_view", self.is_in_item_view, PySI.DataType.BOOL)
        self.set_QML_data("icon_view", self.is_in_icon_view, PySI.DataType.BOOL)
        self.set_QML_data("read_view", self.is_in_read_view, PySI.DataType.BOOL)
        self.set_QML_data("widget_width", self.width, PySI.DataType.INT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.INT)
        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
        self.set_QML_data("is_unread", self.is_unread, PySI.DataType.BOOL)

    def on_double_clicked(self):
        if self.is_in_icon_view and not self.is_in_read_view and not self.is_in_item_view:
            self.to_read_view()

        elif not self.is_in_icon_view and self.is_in_read_view and not self.is_in_item_view:
            self.to_icon_view()

    @SIEffect.on_enter(E.capability.preview_previewing, SIEffect.RECEPTION)
    def on_preview_enter_recv(self):
        if self.is_in_icon_view and not self.is_in_read_view and not self.is_in_item_view:
            self.to_read_view()
            self.snap_to_mouse()

    @SIEffect.on_leave(E.capability.preview_previewing, SIEffect.RECEPTION)
    def on_preview_leave_recv(self):
        if not self.is_in_icon_view and self.is_in_read_view and not self.is_in_item_view:
            self.to_icon_view()
            self.snap_to_mouse()

