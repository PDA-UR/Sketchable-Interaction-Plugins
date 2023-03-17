from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.File import File
from plugins.E import E
from PIL import Image


class ImageFile(File):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ImageFile __"
    region_display_name = "ImageFile"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ImageFile, self).__init__(shape, uuid, "res/image.png", ImageFile.regiontype, ImageFile.regionname, kwargs)

        self.qml_path = self.set_QML_path("ImageFile.qml")
        self.image: SIEffect.SI_CONDITION = True
        self.is_in_preview = False
        self.img_width, self.img_height = Image.open(self.path).size if self.path != "" else Image.open(self.texture_path).size

        self.set_QML_data("is_in_preview", self.is_in_preview, PySI.DataType.BOOL)

        if self.path != "":
            self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
        else:
            self.set_QML_data("img_path", self.texture_path, PySI.DataType.STRING)
        pass

    def to_preview(self):
        self.is_in_preview = True
        x = self.aabb[0].x
        y = self.aabb[0].y

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
        self.set_QML_data("name", self.entryname, PySI.DataType.STRING)

    def to_icon(self):
        self.is_in_preview = False

        self.width = self.icon_width
        self.height = self.icon_height

        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
        self.set_QML_data("container_width", self.width, PySI.DataType.INT)
        self.set_QML_data("container_height", self.height, PySI.DataType.INT)
        self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
        self.set_QML_data("name", self.entryname, PySI.DataType.STRING)
        self.set_QML_data("img_path", self.path, PySI.DataType.STRING)
        self.set_QML_data("is_in_preview", False, PySI.DataType.BOOL)

    @SIEffect.on_leave("ADD_TO_FOLDERBUBBLE", SIEffect.RECEPTION)
    def on_add_to_folder_leave_recv(self):
        self.set_QML_data("is_overlay_visible", True, PySI.DataType.BOOL)

    @SIEffect.on_continuous("ADD_TO_FOLDERBUBBLE", SIEffect.RECEPTION)
    def on_add_to_folder_continuous_recv(self):
        self.set_QML_data("is_overlay_visible", False, PySI.DataType.BOOL)

    @SIEffect.on_enter(E.capability.preview_previewing, SIEffect.RECEPTION)
    def on_preview_enter_recv(self):
        if not self.is_in_preview:
            self.to_preview()
            self.snap_to_mouse()

    @SIEffect.on_leave(E.capability.preview_previewing, SIEffect.RECEPTION)
    def on_preview_leave_recv(self):
        if self.is_in_preview:
            self.to_icon()
            self.snap_to_mouse()

    def on_double_clicked(self):
        if self.parent is None:
            if self.is_in_preview:
                self.to_icon()
            else:
                self.to_preview()

            return True

        return False
