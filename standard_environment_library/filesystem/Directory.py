from libPySI import PySI
from plugins.standard_environment_library.filesystem.Entry import Entry
from plugins.standard_environment_library.button import Button
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
import re


class Directory(Entry):
    regiontype = PySI.EffectType.SI_DIRECTORY
    regionname = PySI.EffectName.SI_STD_NAME_DIRECTORY
    region_width = 130
    region_height = 125

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Directory, self).__init__(shape, uuid, Directory.regiontype, Directory.regionname, kwargs)

        self.qml_path = self.set_QML_path("Directory.qml")
        self.preview_width = 400
        self.preview_height = 600
        self.width = Directory.region_width
        self.height = Directory.region_height
        self.is_icon_visible = True
        self.is_opened_visible = False
        self.children_paths_and_types = [(t[0], t[1] if t[1] != int(PySI.EffectType.SI_UNKNOWN_FILE) else int(PySI.EffectType.SI_TEXT_FILE)) for t in kwargs["children"]]

        self.children = []
        self.num_children_per_page = 6

        self.children_paths_and_types.sort()
        self.current_page = 0

        self.browse_pages = []
        for i in range(len(self.children_paths_and_types)):
            if i % self.num_children_per_page == 0:
                self.browse_pages.append([])

            self.browse_pages[-1].append(self.children_paths_and_types[i])

        self.btn_presses = 0

        self.set_QML_data("container_width", self.width, PySI.DataType.INT)
        self.set_QML_data("container_height", self.height, PySI.DataType.INT)
        self.set_QML_data("img_path", "res/dir.png", PySI.DataType.STRING)
        self.set_QML_data("fullname", self.filename, PySI.DataType.STRING)
        self.set_QML_data("is_visible", self.is_visible, PySI.DataType.BOOL)
        self.set_QML_data("is_icon_visible", self.is_icon_visible, PySI.DataType.BOOL)
        self.set_QML_data("is_opened_visible", self.is_opened_visible, PySI.DataType.BOOL)
        self.set_QML_data("page_name", "1 / " + str(len(self.browse_pages)), PySI.DataType.STRING)

        self.is_open_entry_capability_blocked = False
        self.is_slides = False

    def set_folder_contents_page(self, value):
        self.btn_presses = self.btn_presses - 1 if value else self.btn_presses + 1
        self.current_page = self.btn_presses % len(self.browse_pages)

        if self.btn_presses % len(self.browse_pages) == 0:
            self.btn_presses = 0

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    def on_btn_trigger(self, sender, value):
        self.set_folder_contents_page(value)

        for child in self.children:
            child.delete()

        self.set_QML_data("page_name", str(self.current_page + 1) + "/" + str(len(self.browse_pages)), PySI.DataType.STRING)

        if not self.is_slides:
            self.show_current_folder_contents_page()
        # else:
        #     dir_x = self.absolute_x_pos()
        #     dir_y = self.absolute_y_pos()
        #
        #     dir_width = 1280
        #     dir_height = 720
        #
        #     offset_x = 110
        #     offset_y = 65
        #
        #     entry_shape = [[dir_x + offset_x, dir_y + offset_y + offset_y], [dir_x + offset_x, dir_y + dir_height + offset_y], [dir_x + dir_width + offset_x, dir_y + dir_height + offset_y], [dir_x + dir_width + offset_x, dir_height + offset_y]]
        #
        #     entry = self.browse_pages[self.current_page][0]
        #
        #     kwargs = {}
        #
        #     kwargs["parent"] = self._uuid
        #     kwargs["cwd"] = entry[0]
        #     kwargs["is_slide"] = True
        #
        #     self.create_region_via_id(entry_shape, entry[1], kwargs)
        #
        #     self.add_child_buttons(dir_x, dir_y)

    @SIEffect.on_enter(PySI.CollisionCapability.BTN, SIEffect.RECEPTION)
    def on_btn_enter_recv(self, cursor_id, link_attrib):
        pass

    @SIEffect.on_continuous(PySI.CollisionCapability.BTN, SIEffect.RECEPTION)
    def on_btn_continuous_recv(self, cursor_id, value):
        if cursor_id != "" and value != "":
            self.on_btn_trigger(cursor_id, value)

    @SIEffect.on_leave(PySI.CollisionCapability.BTN, SIEffect.RECEPTION)
    def on_btn_leave_recv(self, cursor_id, link_attrib):
        pass

    def on_open_entry_enter_recv(self, is_other_controlled):
        self.is_slides = False
        self.preview_width = 400
        self.preview_height = 600
        self.num_children_per_page = 6

        self.browse_pages = []
        for i in range(len(self.children_paths_and_types)):
            if i % self.num_children_per_page == 0:
                self.browse_pages.append([])

            self.browse_pages[-1].append(self.children_paths_and_types[i])

    def on_open_entry_continuous_recv(self, is_other_controlled):
        if self.parent == "" and not self.is_open_entry_capability_blocked and not self.is_under_user_control and not is_other_controlled:
            x = self.relative_x_pos()
            y = self.relative_y_pos()

            self.width = self.preview_width
            self.height = self.preview_height

            self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])

            self.is_icon_visible = False
            self.is_opened_visible = True
            self.with_border = True


            self.color = PySI.Color(250, 250, 250, 255)
            self.set_QML_data("container_width", self.width, PySI.DataType.INT)
            self.set_QML_data("container_height", self.height, PySI.DataType.INT)
            self.set_QML_data("is_icon_visible", self.is_icon_visible, PySI.DataType.BOOL)
            self.set_QML_data("is_opened_visible", self.is_opened_visible, PySI.DataType.BOOL)

            self.show_current_folder_contents_page()

            self.is_open_entry_capability_blocked = True

    def on_open_entry_leave_recv(self, is_other_controlled):
        if self.parent == "" and self.is_open_entry_capability_blocked:
            x = self.relative_x_pos()
            y = self.relative_y_pos()

            self.width = self.icon_width * 2
            self.height = self.icon_height + self.text_height

            self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])

            self.is_icon_visible = True
            self.is_opened_visible = False
            self.color = PySI.Color(25, 0, 0, 0)
            self.with_border = False
            self.set_QML_data("container_width", self.width, PySI.DataType.INT)
            self.set_QML_data("container_height", self.height, PySI.DataType.INT)
            self.set_QML_data("is_icon_visible", self.is_icon_visible, PySI.DataType.BOOL)
            self.set_QML_data("is_opened_visible", self.is_opened_visible, PySI.DataType.BOOL)
            self.is_open_entry_capability_blocked = False

            for child in self.children:
                child.delete()

            self.snap_to_mouse()

    # @SIEffect.on_enter(E.id.slideshow_capability_show, SIEffect.RECEPTION)
    # def on_slideshow_enter_recv(self, is_other_controlled):
    #     self.is_slides = True
    #     self.browse_pages = []
    #     for i in range(len(self.children_paths_and_types)):
    #         self.browse_pages.append([self.children_paths_and_types[i]])
    #
    #     self.browse_pages.sort(key=lambda f: int(re.sub('\D', '', f[0][0])))
    #     self.set_QML_data("page_name", "1 / " + str(len(self.browse_pages)), PySI.DataType.STRING)
    #
    #
    # @SIEffect.on_continuous(E.id.slideshow_capability_show, SIEffect.RECEPTION)
    # def on_slideshow_continuous_recv(self, is_other_controlled):
    #     if self.parent == "" and not self.is_open_entry_capability_blocked and not self.is_under_user_control and not is_other_controlled:
    #         x = self.relative_x_pos()
    #         y = self.relative_y_pos()
    #
    #         self.width = 1500
    #         self.height = 882
    #         self.preview_width = self.width
    #         self.preview_height = self.height
    #
    #         self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])
    #
    #         self.is_icon_visible = False
    #         self.is_opened_visible = True
    #         self.with_border = True
    #
    #         self.color = PySI.Color(250, 250, 250, 255)
    #         self.set_QML_data("container_width", self.width, PySI.DataType.INT)
    #         self.set_QML_data("container_height", self.height, PySI.DataType.INT)
    #         self.set_QML_data("is_icon_visible", self.is_icon_visible, PySI.DataType.BOOL)
    #         self.set_QML_data("is_opened_visible", self.is_opened_visible, PySI.DataType.BOOL)
    #
    #         dir_x = self.absolute_x_pos()
    #         dir_y = self.absolute_y_pos()
    #
    #         dir_width = 1280
    #         dir_height = 720
    #
    #         offset_x = 110
    #         offset_y = 65
    #
    #         entry_shape = [[dir_x + offset_x, dir_y + offset_y + offset_y], [dir_x + offset_x, dir_y + dir_height + offset_y], [dir_x + dir_width + offset_x, dir_y + dir_height + offset_y], [dir_x + dir_width + offset_x, dir_height + offset_y]]
    #
    #         entry = self.browse_pages[self.current_page][0]
    #
    #         kwargs = {}
    #
    #         kwargs["parent"] = self._uuid
    #         kwargs["cwd"] = entry[0]
    #         kwargs["is_slide"] = True
    #
    #         self.create_region_via_id(entry_shape, entry[1], kwargs)
    #
    #         self.add_child_buttons(dir_x, dir_y)
    #
    #         self.is_open_entry_capability_blocked = True
    #
    # @SIEffect.on_leave(E.id.slideshow_capability_show, SIEffect.RECEPTION)
    # def on_slideshow_leave_recv(self, is_other_controlled):
    #     if self.parent == "" and self.is_open_entry_capability_blocked:
    #         x = self.relative_x_pos()
    #         y = self.relative_y_pos()
    #
    #         self.width = self.icon_width * 2
    #         self.height = self.icon_height + self.text_height
    #
    #         self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])
    #
    #         self.is_icon_visible = True
    #         self.is_opened_visible = False
    #         self.color = PySI.Color(25, 0, 0, 0)
    #         self.with_border = False
    #         self.set_QML_data("container_width", self.width, PySI.DataType.INT)
    #         self.set_QML_data("container_height", self.height, PySI.DataType.INT)
    #         self.set_QML_data("is_icon_visible", True, PySI.DataType.BOOL)
    #         self.set_QML_data("is_opened_visible", self.is_opened_visible, PySI.DataType.BOOL)
    #         self.is_open_entry_capability_blocked = False
    #
    #         for child in self.children:
    #             child.delete()
    #
    #         self.snap_to_mouse()

    @SIEffect.on_enter(PySI.CollisionCapability.PARENT, SIEffect.EMISSION)
    def on_parent_enter_emit(self, other):
        if self.is_open_entry_capability_blocked and self.parent == "" and not other.is_open_entry_capability_blocked:
            if other not in self.children:
                self.children.append(other)

            return self._uuid

        return ""

    @SIEffect.on_leave(PySI.CollisionCapability.PARENT, SIEffect.EMISSION)
    def on_parent_leave_emit(self, other):
        if self.is_open_entry_capability_blocked and self.parent == "" and not other.is_open_entry_capability_blocked:
            if other in self.children:
                del self.children[self.children.index(other)]

            return self._uuid

        return ""

    # @SIEffect.on_enter(PySI.CollisionCapability.PARENT, SIEffect.RECEPTION)
    def on_parent_enter_recv(self, _uuid):
        if _uuid != "" and not self.is_open_entry_capability_blocked:
            if self.parent == "":
                self.parent = _uuid
                self.create_link(_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    # @SIEffect.on_leave(PySI.CollisionCapability.PARENT, SIEffect.RECEPTION)
    def on_parent_leave_recv(self, _uuid):
        if _uuid != "" and not self.is_open_entry_capability_blocked:
            if self.parent == _uuid:
                self.remove_link(self.parent, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
                self.parent = ""

    def show_current_folder_contents_page(self):
        dir_x = self.absolute_x_pos()
        dir_y = self.absolute_y_pos()

        self.add_child_entries(dir_x, dir_y)
        self.add_child_buttons(dir_x, dir_y)

    def add_child_entries(self, dir_x, dir_y):
        dir_width = self.icon_width * 2
        dir_height = self.icon_height + self.text_height
        x_offset = self.preview_width / 10
        y_offset = self.preview_height / 6
        y_offset2 = dir_height / 12

        i = 0
        y = -1
        x = 1

        for i in range(len(self.browse_pages[self.current_page])):
            entry = self.browse_pages[self.current_page][i]

            if i & 1:
                x += 1
            else:
                x -= 1
                y += 1

            entry_shape = [[((x_offset + dir_width) * x) + (dir_x + x_offset), ((y_offset2 + dir_height) * y) + (dir_y + y_offset)],
                           [((x_offset + dir_width) * x) + (dir_x + x_offset), ((y_offset2 + dir_height) * y) + (dir_y + y_offset + dir_height)],
                           [((x_offset + dir_width) * x) + (dir_x + x_offset + dir_width), ((y_offset2 + dir_height) * y) + (dir_y + y_offset + dir_height)],
                           [((x_offset + dir_width) * x) + (dir_x + x_offset + dir_width), ((y_offset2 + dir_height) * y) + (dir_y + y_offset)]]

            kwargs = {}

            kwargs["parent"] = self._uuid
            kwargs["cwd"] = entry[0]

            self.create_region_via_id(entry_shape, entry[1], kwargs)

    def add_child_buttons(self, dir_x, dir_y):
        horizontal_margin = 10
        vertical_margin = 10

        btn_width = Button.Button.region_width
        btn_height = Button.Button.region_height

        shape_btn1 = [[dir_x + self.preview_width - btn_width - horizontal_margin, dir_y + self.preview_height - btn_height - vertical_margin],
                      [dir_x + self.preview_width - btn_width - horizontal_margin, dir_y + self.preview_height - vertical_margin],
                      [dir_x + self.preview_width - horizontal_margin, dir_y + self.preview_height - vertical_margin],
                      [dir_x + self.preview_width - horizontal_margin, dir_y + self.preview_height - btn_height - vertical_margin]]

        kwargs_btn1 = {}
        kwargs_btn1["parent"] = self._uuid
        kwargs_btn1["value"] = False

        self.create_region_via_id(shape_btn1, PySI.EffectType.SI_BUTTON, kwargs_btn1)

        shape_btn2 = [[dir_x + horizontal_margin, dir_y + self.preview_height - btn_height - vertical_margin],
                      [dir_x + horizontal_margin, dir_y + self.preview_height - vertical_margin],
                      [dir_x + btn_width + horizontal_margin, dir_y + self.preview_height - vertical_margin],
                      [dir_x + btn_width + horizontal_margin, dir_y + self.preview_height - btn_height - vertical_margin]]

        kwargs_btn2 = {}
        kwargs_btn2["parent"] = self._uuid
        kwargs_btn2["value"] = True

        self.create_region_via_id(shape_btn2, PySI.EffectType.SI_BUTTON, kwargs_btn2)
