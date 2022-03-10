from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.AbstractFile import AbstractFile
from plugins.E import E

import os
from PIL import Image


class ImageFile(AbstractFile):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__IMAGE_FILE__"
    region_display_name = "Image File"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "res/image.png", ImageFile.regiontype, ImageFile.regionname, kwargs)
        self.qml_path = self.set_QML_path("ImageFile.qml")
        self.image: SIEffect.SI_CONDITION = True
        self.is_in_preview = False
        self.text_height = 50
        self.is_visible = True
        self.is_set = False
        self.no_preview_width = self.width
        self.no_preview_height = self.height
        self.preview_width = self.width
        self.preview_height = self.height
        self.is_container_visible = True
        self.parent_level = -1 if "hierarchy_level" not in kwargs.keys() else kwargs["hierarchy_level"]
        self.img_width, self.img_height = Image.open(self.path).size if self.path != "" else (0, 0)
        if self.path == "":
            self.adjust_path_for_duplicate()

        if self.img_width != 0 and self.img_height != 0:
            self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
            self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
            self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
            self.set_QML_data("name", self.filename, PySI.DataType.STRING)
            self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
            self.set_QML_data("is_visible", self.is_visible, PySI.DataType.BOOL)
            self.set_QML_data("is_in_preview", self.is_in_preview, PySI.DataType.BOOL)

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y, kwargs={}):
        self.move(self.x + rel_x, self.y + rel_y)
        self.delta_x, self.delta_y = rel_x, rel_y
        self.transform_x += int(self.delta_x)
        self.transform_y += int(self.delta_y)

        if self.is_under_user_control:
            self.mouse_x = abs_x
            self.mouse_y = abs_y
        else:
            self.mouse_x = 0
            self.mouse_y = 0

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        container_width = self.get_QML_data("container_width", PySI.DataType.FLOAT)
        container_height = self.get_QML_data("container_height", PySI.DataType.FLOAT)

        if container_width != 0 and container_height != 0:
            if self.is_new([container_width, container_height], ["container_width", "container_height"]):
                self.shape = PySI.PointVector(
                    [[self.aabb[0].x, self.aabb[0].y],
                     [self.aabb[0].x, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y]
                     ]
                )

                if container_width != 0 and container_height != 0 and not self.is_set:
                    self.no_preview_width = int(container_width)
                    self.no_preview_height = int(container_height)
                    self.is_set = True

                self.width = int(container_width)
                self.height = int(container_height)
                self.is_ready = True
                if self.parent is not None:
                    self.move(self.parent.x + self.x, self.parent.y + self.y)

        self.rename()

    @SIEffect.on_enter(E.capability.preview_previewing, SIEffect.RECEPTION)
    def on_preview_enter_recv(self):
        if not self.is_in_preview:
            self.is_in_preview = True

            x = self.relative_x_pos()
            y = self.relative_y_pos()

            self.width = int(self.img_height / 2 * (self.img_width / self.img_height))
            self.height = int(self.img_height / 2)

            self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])

            self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
            self.set_QML_data("is_in_preview", self.is_in_preview, PySI.DataType.BOOL)
            self.set_QML_data("container_width", self.width, PySI.DataType.INT)
            self.set_QML_data("container_height", self.height, PySI.DataType.INT)
            self.set_QML_data("icon_width", self.width, PySI.DataType.INT)
            self.set_QML_data("icon_height", self.height, PySI.DataType.INT)
            self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
            self.set_QML_data("name", self.filename, PySI.DataType.STRING)

            self.snap_to_mouse()

    @SIEffect.on_leave(E.capability.preview_previewing, SIEffect.RECEPTION)
    def on_preview_leave_recv(self):
        if self.is_in_preview:
            self.color = PySI.Color(10, 0, 0, 0)

            self.is_in_preview = False

            self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
            self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
            self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
            self.set_QML_data("name", self.filename, PySI.DataType.STRING)
            self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
            self.set_QML_data("is_in_preview", False, PySI.DataType.BOOL)

            if self.is_under_user_control:
                self.x = self.mouse_x - self.relative_x_pos() - self.no_preview_width / 2
                self.y = self.mouse_y - self.relative_y_pos() - self.no_preview_height / 2

    @SIEffect.on_leave(E.capability.image_editor_grab_image, SIEffect.RECEPTION)
    def on_grab_image_leave_recv(self):
        self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
