from libPySI import PySI
from plugins.standard_environment_library.filesystem.Entry import Entry
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E

from PIL import Image


class ImageFile(Entry):
    regiontype = PySI.EffectType.SI_IMAGE_FILE
    regionname = PySI.EffectName.SI_STD_NAME_IMAGEFILE

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ImageFile, self).__init__(shape, uuid, ImageFile.regiontype, ImageFile.regionname, kwargs)
        self.qml_path = self.set_QML_path("ImageFile.qml")
        self.is_in_preview = False
        self.image = True

        self.img_width, self.img_height = Image.open(self.path).size if self.path != "" else (0, 0)

        self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
        self.set_QML_data("is_visible", self.is_visible, PySI.DataType.BOOL)
        self.set_QML_data("is_in_preview", self.is_in_preview, PySI.DataType.BOOL)

    @SIEffect.on_enter(E.id.preview_capability_previewing, SIEffect.RECEPTION)
    def on_preview_enter_recv(self):
        if not self.is_in_preview and self.parent == "":
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

            self.snap_to_mouse()

    @SIEffect.on_leave(E.id.preview_capability_previewing, SIEffect.RECEPTION)
    def on_preview_leave_recv(self):
        if self.is_in_preview and self.parent == "":
            self.color = PySI.Color(10, 0, 0, 0)

            self.is_in_preview = False

            x = self.relative_x_pos()
            y = self.relative_y_pos()

            self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
            self.set_QML_data("is_in_preview", self.is_in_preview, PySI.DataType.BOOL)
            self.set_QML_data("container_width", self.width, PySI.DataType.INT)
            self.set_QML_data("container_height", self.height, PySI.DataType.INT)
            self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
            self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)

            self.width = self.icon_width * 2
            self.height = self.icon_height + self.text_height

            self.shape = PySI.PointVector([[x, y], [x, y + self.height],
                                           [x + self.width, y + self.height], [x + self.width, y]])

            if self.is_under_user_control:
                self.snap_to_mouse()

    @SIEffect.on_leave(E.id.image_editor_capability_grab_image, SIEffect.RECEPTION)
    def on_grab_image_leave_recv(self):
        self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
