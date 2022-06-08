from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
import time, threading
from plugins.standard_environment_library.email.InboxItem import InboxItem
import random
from random import choice


class Inbox(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Inbox __"
    region_display_name = "Email Inbox"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Inbox, self).__init__(shape, uuid, "res/email.png", Inbox.regiontype, Inbox.regionname, kwargs)

        self.qml_path = self.set_QML_path("Inbox.qml")
        self.color = PySI.Color(70, 70, 70, 255)
        self.is_timer_running = False
        self.relative_width = 0.33
        self.height_offset = 200
        cw, ch = self.context_dimensions()
        x, y = self.aabb[0].x, self.aabb[0].y
        tw, th = cw * self.relative_width, ch - self.height_offset
        self.email_addition_time = 0.1
        self.max_num_inbox_items_in_inbox = 10

        self.shape = PySI.PointVector([[x, y], [x, y + th], [x + tw, y + th], [x + tw, y]])
        self.width = int(cw * self.relative_width)
        self.target_height = int(ch - self.height_offset)
        self.num_items = 0
        self.num_unread_items = 0

        self.start_y_inbox_items = 180 * ch / 1080
        self.yoffset = ch / 216
        self.xoffset = cw / 48
        self.inbox_item_height = (self.target_height - self.start_y_inbox_items - self.yoffset * self.max_num_inbox_items_in_inbox) / self.max_num_inbox_items_in_inbox
        self.inbox_items = []

        self.email_options = [{"email_sender": "1",
                               "email_receiver": "Mich <juergen.hahn@ur.de>",
                               "email_subject": "TEST1",
                               "message": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
                               "is_unread": True},
                              {"email_sender": "2",
                               "email_receiver": "Mich <juergen.hahn@ur.de>",
                               "email_subject": "TEST2",
                               "message": "2",
                               "is_unread": True},
                              {"email_sender": "3",
                               "email_receiver": "Mich <juergen.hahn@ur.de>",
                               "email_subject": "TEST3",
                               "message": "3",
                               "is_unread": True},
                              {"email_sender": "4",
                               "email_receiver": "Mich <juergen.hahn@ur.de>",
                               "email_subject": "TEST4",
                               "message": "4",
                               "is_unread": True},
                              {"email_sender": "5",
                                "email_receiver": "Mich <juergen.hahn@ur.de>",
                                "email_subject": "TEST5",
                               "message": "5",
                               "is_unread": True}
                              ]
        self.chosen_email_options = []

        self.height = int(self.start_y_inbox_items + self.yoffset)

        self.set_QML_data("img_width", self.texture_width, PySI.DataType.INT)
        self.set_QML_data("img_height", self.texture_height, PySI.DataType.INT)
        self.set_QML_data("img_path", self.texture_path, PySI.DataType.STRING)
        self.set_QML_data("width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("height", self.height, PySI.DataType.FLOAT)
        self.set_QML_data("num_unread_emails", self.num_unread_items, PySI.DataType.FLOAT)
        self.set_QML_data("num_emails", self.num_items, PySI.DataType.FLOAT)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        if not self.is_timer_running:
            self.add_new_email_inbox_item()
            self.is_timer_running = True
            if self.num_items < self.max_num_inbox_items_in_inbox:
                threading.Timer(self.email_addition_time, self.timer_callback).start()

    def timer_callback(self):
        self.is_timer_running = False

    def add_new_email_inbox_item(self):
        try:
            email_option = choice([i for i in range(0, len(self.email_options)) if i not in self.chosen_email_options])
            self.chosen_email_options.append(email_option)
        except:
            email_option = 0

        x, y = self.aabb[0].x + self.x + self.xoffset / 2, self.aabb[0].y + self.y + self.start_y_inbox_items + self.num_items * (self.inbox_item_height + self.yoffset)
        shape = [[x, y], [x, y + self.inbox_item_height], [x + self.width - self.xoffset, y + self.inbox_item_height], [x + self.width - self.xoffset, y]]

        self.adjust_shape_and_height(self.height + self.inbox_item_height + self.yoffset)

        self.create_region_via_name(PySI.PointVector(shape), InboxItem.regionname, False, {"parent": self, "data": self.email_options[email_option]})

        self.num_items += 1
        self.num_unread_items += 1
        self.set_QML_data("num_emails", self.num_items, PySI.DataType.FLOAT)
        self.set_QML_data("num_unread_emails", self.num_unread_items, PySI.DataType.FLOAT)

    @SIEffect.on_enter("__INBOX_ENTRY__", SIEffect.EMISSION)
    def on_inbox_entry_enter_emit(self, other):
        pass

    def move_item_to_position_in_inbox(self, other, current_last, idx):
        if idx != len(self.inbox_items) - 1:
            other.move(self.inbox_items[idx + 1].x, self.inbox_items[idx + 1].y + self.inbox_item_height + self.yoffset)
        else:
            other.move(current_last.x, current_last.y)

    def sort_item_into_inbox(self, other):
        other.can_enter = False
        current_last = self.inbox_items[-1]
        self.inbox_items.append(other)
        self.inbox_items.sort(key=lambda x: x.date)
        idx = self.inbox_items.index(other)
        self.move_item_to_position_in_inbox(other, current_last, idx)

        return idx

    @SIEffect.on_continuous("__INBOX_ENTRY__", SIEffect.EMISSION)
    def on_inbox_entry_continuous_emit(self, other):
        if other.was_moved() and other.can_enter:
            other.create_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)
            self.adjust_shape_and_height(self.height + self.inbox_item_height + self.yoffset)
            idx = self.sort_item_into_inbox(other)
            self.rearrange_inbox_items(idx + 1, up=False)
            self.num_items += 1
            if other.is_unread:
                self.num_unread_items += 1
                self.set_QML_data("num_unread_emails", self.num_unread_items, PySI.DataType.FLOAT)
            self.set_QML_data("num_emails", self.num_items, PySI.DataType.FLOAT)

            return True, self

        return False, None

    def adjust_shape_and_height(self, new_height):
        self.height = int(new_height)
        self.shape = PySI.PointVector([[self.aabb[0].x, self.aabb[0].y],
                                       [self.aabb[0].x, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y]])
        self.set_QML_data("height", self.height, PySI.DataType.FLOAT)

    @SIEffect.on_leave("__INBOX_ENTRY__", SIEffect.EMISSION)
    def on_inbox_entry_leave_emit(self, other):
        other.remove_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)
        idx = self.inbox_items.index(other)
        self.inbox_items.remove(other)
        self.adjust_shape_and_height(self.height - self.inbox_item_height - self.yoffset)
        self.rearrange_inbox_items(idx)
        self.num_items -= 1
        self.num_unread_items -= 1
        self.set_QML_data("num_emails", self.num_items, PySI.DataType.FLOAT)
        self.set_QML_data("num_unread_emails", self.num_unread_items, PySI.DataType.FLOAT)

    def rearrange_inbox_items(self, from_idx, up=True):
        for i in range(from_idx, len(self.inbox_items)):
            item = self.inbox_items[i]
            if up:
                item.move(item.x, item.y - self.inbox_item_height - self.yoffset)
            else:
                item.move(item.x, item.y + self.inbox_item_height + self.yoffset)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        for item in self.inbox_items:
            item.delete()
        self.delete()